#!/usr/bin/env python3
"""
Main entrypoint to the script.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from cbdc_scraper.headless_browser import new_scrape


def test_new_scrape():
    check = new_scrape()
    assert True == True