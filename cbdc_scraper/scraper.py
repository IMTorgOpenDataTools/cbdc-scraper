#!/usr/bin/env python3
"""
Main entrypoint to the script.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from logzero import logger

from utils import get_data


def main(args):
    """ Main entry point of the app """
    logger.info("hello world")
    logger.info(args)
    get_data()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    #parser.add_argument("arg", help="Required positional argument")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)