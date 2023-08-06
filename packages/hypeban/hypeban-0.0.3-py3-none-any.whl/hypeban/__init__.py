#!/usr/bin/python3
import argparse
from datetime import datetime
import hypeban

parser = argparse.ArgumentParser()

parser.add_argument("--about", help="display information about program", action="store_true")
parser.add_argument("-s", "--since", help="enter a date as an argument to find days since given date")
parser.add_argument("-u", "--until", help="enter a date as an argument to find days until given date")

args = parser.parse_args()
if args.about:
    print("A terminal-based program that calculates days left until a given date that parses DateStrings in multiple UNIX-compliant formats created by Bupper")

elif args.since:
    date_string = args.since
    hypeban.includes_dashes = hypeban.contains_dashes(date_string)
    if hypeban.includes_dashes: date_string_elements = date_string.split("-")

    if hypeban.includes_dashes and len(date_string_elements[0]) == 4: 
        result = hypeban.days_since_date(date_string, "%Y-%m-%d")
        print("Days since:", result)

    elif hypeban.includes_dashes and len(date_string_elements[-1]) == 4:
        result = hypeban.days_since_date(date_string, "%m-%d-%Y")
        print("Days since:", result)

elif args.until:
    date_string = args.until
    hypeban.includes_dashes = hypeban.contains_dashes(date_string)
    if hypeban.includes_dashes: date_string_elements = date_string.split("-")

    if hypeban.includes_dashes and len(date_string_elements[0]) == 4: 
        result = hypeban.days_until_date(date_string, "%Y-%m-%d")
        print("Days until:", result)

    elif hypeban.includes_dashes and len(date_string_elements[-1]) == 4:
        result = hypeban.days_until_date(date_string, "%m-%d-%Y")
        print("Days until:", result)

else:
    print("No arguments were entered, type hypeban [-h] for help.")