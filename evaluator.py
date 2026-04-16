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