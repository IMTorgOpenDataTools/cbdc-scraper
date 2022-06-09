#!/usr/bin/env python3
"""
Main entrypoint to the script.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
import argparse
from pathlib import Path
import time

from utils import (
    get_data_atlantic,
    get_data_cbdc,
    process_data,
    )
sys.path.append(Path('config').absolute().as_posix() )
from _constants import (
    logger,
    output
)



def main(args):
    """ Main entry point of the app. """
    logger.info("Begin scraping process")
    start_time = time.time()

    # get data
    data_dict = {}
    data_dict_cbdc = get_data_cbdc()
    data_dict_atlantic = get_data_atlantic()
    data_dict.update(data_dict_cbdc)
    data_dict.update(data_dict_atlantic)

    # merge and process
    recs = process_data(data_dict)

    # export
    check = output.create_report(recs=recs)
    if check:
        checks = output.send_notification()
        logger.info(f"result of email notifications: {checks}")
    else:
        logger.error("report failed")
        output.send_notification(error=True)
    logger.info(f"data downloaded: {check}")
    logger.info(f"End scraping process, execution took: {round(time.time() - start_time, 3)}sec")



if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)