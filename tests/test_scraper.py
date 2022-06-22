#!/usr/bin/env python3
"""
Test the Scraper class.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

import pandas as pd



from cbdc_scraper.utils import (
    get_data_cbdc, 
    get_data_atlantic,
    check_dataframes,
    process_data,
    export_data
)


def test_get_data_cbdc():
    data = get_data_cbdc()

    check1 = len(data.keys()) == 5
    check2 = len( list(data.values())[0] ) > 20
    assert all([check1, check2]) == True


def test_get_data_atlantic():
    data = get_data_atlantic()

    assert [*data.keys()] == ['Atlantic']


def test_check_dataframes():
    data_dict = {}
    df = pd.DataFrame()
    data_dict['df'] = df
    check = check_dataframes(data_dict)
    assert check == [False]


def test_process_data():
    """
    expected output: 204 recs
    """
    data_dict = {}
    data_dict_cbdc = get_data_cbdc()
    data_dict_atlantic = get_data_atlantic()
    data_dict.update(data_dict_cbdc)
    data_dict.update(data_dict_atlantic)
    data_dict = process_data(data_dict)
    recs = export_data(data_dict)

    assert len(recs) == 236