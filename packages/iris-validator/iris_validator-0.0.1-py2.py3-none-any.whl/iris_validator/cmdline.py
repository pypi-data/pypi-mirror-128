import os
import re
import sys
import argparse

import logging as logger
logger.basicConfig(level=logger.WARN)

from iris_validator import stationxml_validator
from iris_validator.iris_validate import validate_iris_stationxml_examples_vs_rules

def main():

    fname = 'iris-validator'

    args = process_cmd_line(fname)

    if args.run_tests:
        validate_iris_stationxml_examples_vs_rules()
    else:
        validator = stationxml_validator(args.infile)
        validator.validate_inventory()
        print("[SUMMARY]:")
        print("%7s N_Errors:%d N_Warnings:%d\n" % (' ', len(validator.errors), len(validator.warnings)))
        print("[ERRORS]:\n")
        for msgs in validator.errors:
            for i, msg in enumerate(msgs):
                if i == 0:
                    print(msg)
                else:
                    print("%7s %s" % (' ', msg))
        print("\n[WARNINGS]:\n")
        traditional_msgs = ['1 -', '2 -', '3 -']
        for msgs in validator.warnings:
            for i, msg in enumerate(msgs):
                if msg == '':
                    continue
                indent = True
                for x in traditional_msgs:
                    if x in msg:
                        indent = False
                        break
                if indent:
                    if i == 0:
                        print(msg)
                    else:
                        print("%7s %s" % (' ', msg))
                else:
                    print(msg)
    return

def process_cmd_line(fname):

    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")

    parser._action_groups.append(optional) # 
    group = required.add_mutually_exclusive_group(required=True)

    #required.add_argument("--infile", type=str, metavar='// path-to StationXML file, e.g., --infile=/path/to/foo.xml',
                          #required=True)
    group.add_argument("--infile", type=str, help='// path-to StationXML file, e.g., --infile=/path/to/foo.xml')
    group.add_argument("--run-tests", action='store_true', help='// Run IRIS Validator Test Files')

    #optional.add_argument("--preferred-eventtime", type=UTCDateTime)

    args, unknown = parser.parse_known_args()

    # Check that infile exists:
    if args.infile and not os.path.isfile(args.infile):
        print("Unable to read infile=%s --> Exiting!" % args.infile)
        parser.print_help()
        exit(2)

    return args


if __name__ == "__main__":
    main()
