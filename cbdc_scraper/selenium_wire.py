#!/usr/bin/env python3
"""
Selenium-wire proxy used to get csv from backend.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pathlib import Path
import time



# Options
chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable_encoding')
chrome_options.add_argument('--ignore_http_methods')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--connection_keep_alive')




def selenium_wire_scrape():
    # setup
    #url = "https://www.atlanticcouncil.org/cbdctracker/"                       #get svg url from iframe 
    url = "https://geoecon.github.io/21.10.20-CBDC-Tracker-Update-R1/?params="
    chrome_driver = "./.libs/chromedriver"
    path_driver = Path(chrome_driver).absolute().__str__()
    driver = webdriver.Chrome(path_driver, chrome_options=chrome_options)

    # get url of googledocs data supplier
    driver.get(url)
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    urls = [req.url for req in driver.requests if 'docs.google.com' in req.url]

    return urls