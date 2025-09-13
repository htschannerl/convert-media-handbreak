import argparse

__version__ = "1.0.0"

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("action",choices=["convert","backup"], help="The action you want to act on.")

    args = parser.parse_args()
    return args