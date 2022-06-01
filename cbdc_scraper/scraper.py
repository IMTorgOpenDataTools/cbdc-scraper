#!/usr/bin/env python3
"""
Main entrypoint to the script.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
import argparse
from logzero import logger
from pathlib import Path

from output import Output
from utils import (
    get_data_atlantic,
    get_data_cbdc,
    process_data,
    )
sys.path.append(Path('config').absolute().as_posix() )
from _constants import (
    emails_file,
    report_dir
)



def main(args):
    """ Main entry point of the app. """
    logger.info(args)
    data_dict = {}
    data_dict_cbdc = get_data_cbdc()
    data_dict_atlantic = get_data_atlantic()
    data_dict.update(data_dict_cbdc)
    data_dict.update(data_dict_atlantic)

    recs = process_data(data_dict)

    output = Output(
        report_dir = report_dir,
        emails_file = emails_file
        )
    check = output.create_report(recs=recs)
    if check:
        checks = output.send_notification()
        logger.info(f"result of email notifications: {checks}")
    logger.info(f"data downloaded: {check}")



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