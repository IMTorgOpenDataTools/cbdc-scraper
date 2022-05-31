#!/usr/bin/env python3
"""
Main entrypoint to the script.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from cbdc_scraper.selenium_bmop import selenium_scrape
from cbdc_scraper.selenium_wire import selenium_wire_scrape
from cbdc_scraper.puppet import puppet_scrape


def test_selenium_scrape():
    check = selenium_scrape()
    assert True == True

def test_selenium_wire_scrape():
    check = selenium_wire_scrape()
    assert True == True

def test_puppet_scrape():
    check = puppet_scrape()
    assert True == True