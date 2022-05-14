#!/usr/bin/env python3
"""
Main entrypoint to the script.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from cbdc_scraper.utils import get_data, process_data, download_data


def test_get_data():
    data = get_data()

    check1 = len(data.keys()) == 4
    check2 = len( list(data.values())[0] ) > 20
    assert all([check1, check2]) == True


def test_process_data():
    data_dict = get_data()
    recs = process_data(data_dict)

    assert len(recs) > 10


def test_complete_process():
        data_dict = get_data()
        recs = process_data(data_dict)
        check = download_data(recs)

        assert check == True