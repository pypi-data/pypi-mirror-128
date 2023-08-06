#!/usr/bin/env python3

import akrophonobolos as obol
import argparse
from fractions import Fraction
from sys import exit


def money(s):
    return obol.Khremata(s)


def spread(d, s):
    return range(d - s, d + s + 1)


def calculate_interest(args, rate):
    per_diem = args.principal * rate
    if args.day_range:
        for s in spread(args.days, args.day_range):
            format_output(args.principal,
                          per_diem,
                          s,
                          obol.interest(args.principal, s, rate))
        return

    format_output(args.principal,
                  per_diem,
                  args.days,
                  obol.interest(args.principal, args.days, rate))


def calculate_days(args, rate):
    r = args.principal * rate
    format_output(args.principal,
                  r,
                  (args.interest/r).limit_denominator(1),
                  args.interest)


def calculate_principal(args, rate):
    if args.day_range:
        for s in spread(args.days, args.day_range):
            format_output(obol.principal(args.interest, s, rate),
                          args.interest/s,
                          s,
                          args.interest)
        return

    format_output(obol.principal(args.interest, args.days, rate),
                  args.interest/args.days,
                  args.days,
                  args.interest)


def format_output(p, r, d, i):
    print(f"{p.as_greek()} ({p.as_abbr()}) "
          f"at {r.as_phrase(True)} per day "
          f"for {d} days = "
          f"{i.as_greek()} ({i.as_abbr(True)}) interest")


def get_interest_rate(args):
    return obol.interest_rate(obol.Khremata(args.int_p),
                              obol.Khremata(args.int_i),
                              args.int_d)


def main():
    parser = argparse.ArgumentParser(
        description="Ancient Athenian acrophonic numeral converter"
    )
    parser.add_argument("-p", "--principal", type=money, default=None,
                        help="Amount of principal of loan")
    parser.add_argument("-r", "--rate", type=float, default=1.2,
                        help="Rate of simple interest, expressed as the "
                        "number of obols per talent per day")
    parser.add_argument("-d", "--days", type=int, default=None,
                        help="Number of days of loan")
    parser.add_argument("-i", "--interest", type=money, default=None,
                        help="Interest paid")
    parser.add_argument("--day-range", metavar="DAYS", type=int, default=0,
                        help="Calculate interest for DAYS days before and "
                        "after the -d/--days parameter")
    parser.add_argument("--int-p", metavar="P", default="5t",
                        help="Principal amount for interest rate calculation")
    parser.add_argument("--int-i", metavar="I", default="1d",
                        help="Interest amount for interest rate calculation")
    parser.add_argument("--int-d", metavar="D", default=1, type=int,
                        help="Number of days for interest rate calculation")

    args = parser.parse_args()

    rate = obol.interest_rate(args.int_p, args.int_d, args.int_i)

    if all((args.principal, args.rate, args.days)) and not args.interest:
        calculate_interest(args, rate)
        return

    if all((args.principal, args.rate, args.interest)) and not args.days:
        calculate_days(args, rate)
        return

    if all((args.rate, args.days, args.interest)) and not args.principal:
        calculate_principal(args, rate)
        return


if __name__ == "__main__":
    main()
