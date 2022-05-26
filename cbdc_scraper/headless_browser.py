"""
FAIL

    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/local/python/lib/python3.10/json/encoder.py", line 257, in iterencode
    return _iterencode(o, 0)
  File "/usr/local/python/lib/python3.10/json/encoder.py", line 179, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type PosixPath is not JSON serializable
"""



from selenium import webdriver
from selenium.webdriver.chrome.options import Options



chrome_options = Options()
chrome_options.headless = True

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')

chrome_options.add_argument('--disable-dev-shm-usage')

#chrome_options.binary_location = "C:\\path\\to\\chrome.exe"
chrome_options.add_argument("--start-maximized") #open Browser in maximized mode
#options.add_argument("--no-sandbox") #bypass OS security model
#options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)






from pathlib import Path 




def new_scrape():
    url = "http://zenrows.com" 
    binary = "./.libs/ungoogled-chrome"
    driver = "./.libs/chromedriver"
    path_driver = Path(driver).absolute()
    chrome_options.binary_location = Path(binary).absolute()
    check = path_driver.is_file()
    with webdriver.Chrome(path_driver, chrome_options=chrome_options) as driver:
        driver.get(url)
        print(driver.current_url)       # https://www.zenrows.com/
        print(driver.title)             # Web Scraping API & Data Extraction - ZenRows

    return True

new_scrape()