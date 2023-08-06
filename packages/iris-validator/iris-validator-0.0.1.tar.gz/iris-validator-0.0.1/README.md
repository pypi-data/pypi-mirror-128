# IRIS-validator 

iris-validator is a small python module for validation
stationxml files against the IRIS StationXML Validation Rules found at:

https://github.com/iris-edu/stationxml-validator/wiki/StationXML-Validation-Rule-List

It has a limited API and a command-line script


## Installation

### Requirements

    obspy >= 1.2

These requirements should be automatically installed for you (see below).

### Install

Clone the repository and install:

    >git clone https@gitlab.isti.com:mhagerty/iris-validator.git 
    >cd iris-validator
    >pip install .


### Usage:

Once you have installed it, you should be able to run it as a python module from any directory.

    >iris-validator

    usage: iris-validator [-h] (--infile INFILE | --run-tests)
    iris-validator: error: one of the arguments --infile --run-tests is required

    options:
    --infile=..     //specify path to stationxml file
    --run-tests     //will step through IRIS validation test files (e.g., F1_423.xml)
                      and test each against the appropriate rule


    > iris-validator --run-tests
    Check file:F1_101.xml against Rule:101
    SUCCESS: xmlfile=[F1_101.xml] FAILED as expected
    Check file:F1_110.xml against Rule:110
    SUCCESS: xmlfile=[F1_110.xml] FAILED as expected
    Check file:F2_110.xml against Rule:110 
    SUCCESS: xmlfile=[F2_110.xml] FAILED as expected
    ...
    Check file:P1_112.xml against Rule:112
    SUCCESS: xmlfile=[P1_112.xml] PASSED as expected
    ...
    Check file:F1_422.xml against Rule:422 
    SUCCESS: xmlfile=[F1_422.xml] FAILED as expected
    Check file:F1_423.xml against Rule:423
    SUCCESS: xmlfile=[F1_423.xml] FAILED as expected

### API
To use the module from within your own python script, follow the example
below:

    from iris_validator import stationxml_validator

    validator = stationxml_validator('path/to/some/stationxml.xml')

    validator.validate_inventory()

    print("[ERRORS]:\n")
    for msgs in validator.errors:
        for i, msg in enumerate(msgs):
            if i == 0:
                print(msg)
            else:
                print("%7s %s" % (' ', msg))

    print("\n[WARNINGS]:\n")
    for msgs in validator.warnings:
        for i, msg in enumerate(msgs):
            if i == 0:
                print(msg)
            else:
                print("%7s %s" % (' ', msg))

Note some other things you can do include:

    validator.validate_rule('420')          // You can test your stationxml file against one rule at a time
