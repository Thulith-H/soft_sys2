"""
Pipeline for each expression:
    tokenize()  -->  parse()  -->  tree_to_string() + evaluate()  -->  output """

import os
import sys



def make_token(token_type, value):
    """
    Create a single token as a dictionary.
    A dictionary like {"type": "NUM", "value": 3.0} """

    return {"type": token_type, "value": value}


def tokenize(expression):
    """
    Turn a raw expression string into a list of tokens.
    Scans left to right, skips whitespace, and labels each character or
    group of characters with its token type. ValueError if an unexpected character is found """

    tokens = []
    i = 0  # current position in the string

    while i < len(expression):
        char = expression[i]

        # skip spaces and tabs, nothing to do here
        if char == " " or char == "\t":
            i += 1
            continue

        # if it starts with a digit or dot, read the whole number
        if char.isdigit() or char == ".":
            start = i  # remember where the number started
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            number_str = expression[start:i]  # slice out the full number e.g. "3.14"
            tokens.append(make_token("NUM", float(number_str)))
            continue

        # single character operators
        if char in ("+", "-", "*", "/"):
            tokens.append(make_token("OP", char))
            i += 1
            continue

        # opening bracket starts a sub-expression
        if char == "(":
            tokens.append(make_token("LPAREN", "("))
            i += 1
            continue

        # closing bracket ends a sub-expression
        if char == ")":
            tokens.append(make_token("RPAREN", ")"))
            i += 1
            continue

        # anything else like @ or # is not valid
        raise ValueError(f"Unexpected character: '{char}'")

    # always add END so the parser knows when to stop
    tokens.append(make_token("END", None))
    return tokens

# TREE NODES
# Constructor functions that build tree node dictionaries.
def make_num_node(value):
    """
    Create a leaf node for a number literal. """

    return {"type": "num", "value": value}


def make_binary_operation_node(op, left, right):
    """
    Create a node for a binary operation (two operands).
    op    : string one of "+", "-", "*", "/"
    left  : the left-hand tree node
    right : the right-hand tree node   """

    return {"type": "bin-op", "op": op, "left": left, "right": right}


def make_neg_node(operand):
    """
    Create a node for unary negation. """

    return {"type": "neg", "operand": operand}



# PARSER (Recursive Descent)
# Converts a token list into a parse tree.
# Call chain (lowest to highest priority):
#   parse_expression --> parse_term --> parse_unary --> parse_primary


def make_parser_state(tokens):
    """
    Create a state dictionary to track our position in the token list. """

    return {"tokens": tokens, "pos": 0}


def current_token(state):
    """
    Return the token we are currently looking at, without moving forward. """
    return state["tokens"][state["pos"]]


def consume_token(state):
    """
    Return the current token and move forward to the next one. """

    token = state["tokens"][state["pos"]]
    state["pos"] += 1  # move the cursor one step forward
    return token


def parse_primary(state):
    """
    Parse the highest-priority items: numbers and parenthesised expressions. """
    token = current_token(state)

    # plain number, just wrap it in a node and move on
    if token["type"] == "NUM":
        consume_token(state)
        return make_num_node(token["value"])

    # opening paren means we recurse and parse what is inside
    if token["type"] == "LPAREN":
        consume_token(state)                    # move past "("
        node = parse_expression(state)          # recurse back to the top
        closing = current_token(state)
        if closing["type"] != "RPAREN":
            raise ValueError("Expected closing ')'")
        consume_token(state)                    # move past ")"
        return node

    # unary plus is not supported, raise early
    if token["type"] == "OP" and token["value"] == "+":
        raise ValueError("Unary + is not supported")

    # if we get here nothing matched, the expression is broken
    raise ValueError(f"Unexpected token: {token}")


def parse_unary(state):
    """
    Parse unary negation: -5, --5, -(3+4) """
    token = current_token(state)

    # found a minus, wrap whatever comes next in a neg node
    if token["type"] == "OP" and token["value"] == "-":
        consume_token(state)                    # move past "-"
        operand = parse_unary(state)            # recurse so --5 works naturally
        return make_neg_node(operand)

    # no minus here, hand off to primary
    return parse_primary(state)


def parse_term(state):
    """
    Parse multiplication and division: 3 * 4, 10 / 2

    Also handles implicit multiplication: 4(3+1) means 4 * (3+1)
    If after a value we see "(" with no operator, we treat it as "*".
    """
    left = parse_unary(state)

    while True:
        token = current_token(state)

        # explicit star or slash, consume and build a binop node
        if token["type"] == "OP" and token["value"] in ("*", "/"):
            consume_token(state)
            right = parse_unary(state)
            left = make_binary_operation_node(token["value"], left, right)

        # no operator but a paren follows, treat it as implicit multiply
        elif token["type"] == "LPAREN":
            right = parse_primary(state)     # parse the (...) group
            left = make_binary_operation_node("*", left, right)

        # nothing matched, no more terms to consume
        else:
            break

    return left

def parse_expression(state):
    """
    Parse addition and subtraction: 3 + 5, 10 - 2 """
    left = parse_term(state)  # always start by parsing the left side

    while True:
        token = current_token(state)
        if token["type"] == "OP" and token["value"] in ("+", "-"):
            consume_token(state)
            right = parse_term(state)  # parse right side the same way
            left = make_binary_operation_node(token["value"], left, right)
        else:
            break  # no more plus or minus, we are done

    return left


def parse(tokens):
    """
    Main entry point for parsing. """
    state = make_parser_state(tokens)
    tree = parse_expression(state)

    # if tokens are left over the expression was malformed e.g. "3 5"
    if current_token(state)["type"] != "END":
        raise ValueError(f"Unexpected token after expression: {current_token(state)}")

    return tree

# EVALUATOR AND TREE PRINTER
# Both walk the tree recursively, one computes a number, one builds a string.


def format_number(value):
    """
    Format a number for display. """
    # drop the decimal if it is a whole number e.g. 8.0 becomes 8
    if value == int(value):
        return str(int(value))
    return str(round(value, 4))  # otherwise round to 4 decimal places


def tree_to_string(node):
    """
    Convert a parse tree into a readable string. """
    # leaf node, just return the number as a string
    if node["type"] == "num":
        return format_number(node["value"])

    # neg node wraps its child in (neg ...)
    if node["type"] == "neg":
        operand_str = tree_to_string(node["operand"])  # recurse on the child
        return f"(neg {operand_str})"

    # binary op puts the operator first then left and right children
    if node["type"] == "bin-op":
        left_str  = tree_to_string(node["left"])   # recurse left
        right_str = tree_to_string(node["right"])  # recurse right
        return f"({node['op']} {left_str} {right_str})"
    else:
        return None


def evaluate(node):
    """
    Walk the parse tree and compute the final numeric result.
    """
    # base case, just return the number stored in the node
    if node["type"] == "num":
        return node["value"]

    # negate whatever the child evaluates to
    if node["type"] == "neg":
        operand_val = evaluate(node["operand"])  # recurse on child
        return -operand_val

    # binary op, evaluate both sides then apply the operator
    if node["type"] == "bin-op":
        left_val  = evaluate(node["left"])   # recurse left
        right_val = evaluate(node["right"])  # recurse right

        if node["op"] == "+":
            return left_val + right_val

        if node["op"] == "-":
            return left_val - right_val

        if node["op"] == "*":
            return left_val * right_val

        if node["op"] == "/":
            if right_val == 0:
                raise ValueError("Division by zero")
            return left_val / right_val

        raise ValueError(f"Unknown operator: {node['op']}")  # should never reach here

    raise ValueError(f"Unknown node type: {node['type']}")   # should never reach here

# FILE I/O
# Reads the input file, processes each expression, writes output.txt.


def tokens_to_string(tokens):
    """
    Convert a list of token dictionaries into a display string. """
    parts = []

    for token in tokens:
        if token["type"] == "END":
            parts.append("[END]")
        elif token["type"] == "NUM":
            parts.append(f"[NUM:{format_number(token['value'])}]")
        else:
            # covers OP, LPAREN, RPAREN
            parts.append(f"[{token['type']}:{token['value']}]")

    return " ".join(parts)


def process_expression(expression):
    """
    Run the full pipeline on a single expression string. """

    # start with ERROR for everything, fill in as we go
    result = {
        "input":  expression,
        "tokens": "ERROR",
        "tree":   "ERROR",
        "result": "ERROR"
    }

    try:
        # step 1 tokenize the raw string
        tokens = tokenize(expression)
        result["tokens"] = tokens_to_string(tokens)

        # step 2 parse the tokens into a tree
        tree = parse(tokens)
        result["tree"] = tree_to_string(tree)

        # step 3 evaluate the tree to get the final number
        value = evaluate(tree)
        result["result"] = value

    except ValueError:
        pass    # something went wrong, keep whatever ERRORs remain

    return result


def format_output_block(result):
    """
    Turn a result dictionary into the four-line output block. """

    if result["result"] == "ERROR":
        result_line = "ERROR"
    else:
        result_line = format_number(result["result"])  # clean number formatting

    lines = [
        f"Input: {result['input']}",
        f"Tree: {result['tree']}",
        f"Tokens: {result['tokens']}",
        f"Result: {result_line}"
    ]

    return "\n".join(lines)


def evaluate_file(input_path):
    """
    Read a file of expressions, evaluate each one, and write output.txt. """

    with open(input_path, "r") as f:
        lines = f.readlines()

    all_results = []

    for line in lines:
        expression = line.strip()  # remove newline characters

        if expression == "":
            continue    # skip blank lines in the input

        result = process_expression(expression)
        all_results.append(result)

    # join all blocks with a blank line between them
    blocks = []
    for result in all_results:
        blocks.append(format_output_block(result))

    output_text = "\n\n".join(blocks)

    # write to the same folder as the input file
    input_dir   = os.path.dirname(os.path.abspath(input_path))
    output_path = os.path.join(input_dir, "output.txt")

    with open(output_path, "w") as f:
        f.write(output_text)

    print(f"Output written to: {output_path}")

    return all_results


# ENTRY POINT
# Run from the command line: python main.py sample_input.txt

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluator.py <input_file>")
    else:
        results = evaluate_file(sys.argv[1])
        for r in results:
            print(format_output_block(r))
            print()