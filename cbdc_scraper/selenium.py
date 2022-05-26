
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument("--start-maximized") #open Browser in maximized mode
chrome_options.add_argument("--no-sandbox") #bypass OS security model
#options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)


from pathlib import Path 




def selenium_scrape():
    url = "https://www.atlanticcouncil.org/cbdctracker/" 
    driver = "./.libs/chromedriver"
    path_driver = Path(driver).absolute().__str__()
    #binary = "./.libs/ungoogled-chrome"
    #chrome_options.binary_location = Path(binary).absolute().__str__()     #not necessary
    with webdriver.Chrome(path_driver, chrome_options=chrome_options) as driver:
        driver.get(url)
        print(driver.current_url)       # https://www.zenrows.com/
        print(driver.title)             # Web Scraping API & Data Extraction - ZenRows

    return True