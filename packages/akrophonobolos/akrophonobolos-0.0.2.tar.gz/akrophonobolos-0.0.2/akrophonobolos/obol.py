#!/usr/bin/env python3

import akrophonobolos as obol
import argparse
from enum import Enum, auto
from sys import exit


class UnexpectedEndOfEquation(Exception):
    pass


class UnexpectedInput(Exception):
    pass


class INPUT_T(Enum):
    ACRO = auto()
    STR = auto()
    OP = auto()
    UNK = auto()


def detect_type(input):
    if any([i in obol.NUMERALS.keys() for i in input]):
        return INPUT_T.ACRO

    if obol.valid_amount_str(input):
        return INPUT_T.STR

    if input in ("+", "-"):
        return INPUT_T.OP

    return INPUT_T.UNK


def is_equation(input):
    return any([detect_type(i) == INPUT_T.OP for i in input])


def recurse_calc(eq):
    if len(eq) == 1:
        return obol.Khremata(eq[0])

    if len(eq) > 1:
        if eq[1] == "+":
            return obol.Khremata(eq[0]) + recurse_calc(eq[2:])

        if eq[1] == "-":
            return obol.Khremata(eq[0]) - recurse_calc(eq[2:])

        raise UnexpectedInput(f"Expected '+' or '-', got '{eq[1]}'")

    raise UnexpectedEndOfEquation()


def do_equation(input):
    result = recurse_calc(input)
    print(f"{result.as_greek()} = {result.as_abbr()}")


def main():
    parser = argparse.ArgumentParser(
        description="Ancient Athenian acrophonic numeral converter"
    )
    parser.add_argument("input", nargs="+", type=str)
    args = parser.parse_args()

    if is_equation(args.input):
        do_equation(args.input)
        exit()

    for i in args.input:
        if detect_type(i) in (INPUT_T.ACRO, INPUT_T.STR):
            p = obol.Khremata(i)

            if detect_type(i) == INPUT_T.ACRO:
                print(f"{i} = {p.as_phrase()}")

            else:
                print(f"{i} = {p.as_greek()}")


if __name__ == "__main__":
    main()
