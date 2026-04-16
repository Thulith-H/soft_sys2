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