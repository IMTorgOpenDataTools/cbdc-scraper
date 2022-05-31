


from seleniumwire import webdriver  # Import from seleniumwire
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
#chrome_options.add_argument({'request_storage': 'memory'})
#chrome_options.add_argument({'request_storage_max_size': '100'})

# Enable Performance Logging of Chrome.
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
desired_capabilities['acceptSslCerts'] = True
desired_capabilities['acceptInsecureCerts'] = True

def interceptor_body(request):
    if 'doc' not in request.url:
        if request.response:
            if request.response.body:
                request.response.body = ''

def interceptor_abort(request, response):
    if 'text/csv' in response.headers['Content-Type']:
        response.headers['Target'] = True
    else:
        request.abort




def selenium_wire_scrape():
    #url = 'https://www.google.com'
    #url = "https://www.atlanticcouncil.org/cbdctracker/" 
    url = "https://geoecon.github.io/21.10.20-CBDC-Tracker-Update-R1/?params="
    chrome_driver = "./.libs/chromedriver"
    path_driver = Path(chrome_driver).absolute().__str__()
    driver = webdriver.Chrome(path_driver, chrome_options=chrome_options)    #, desired_capabilities=desired_capabilities)
    driver.response_interceptor = interceptor_abort
    # Create a new instance of the Chrome driver

    # Go to the Google home page
    #driver.scopes = ['*google*',"*doc*","*geo*"]
    driver.get(url)
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    pat = 'doc-08-0k'
    N = 6
    
    """
    try:
        elem = WebDriverWait(driver, N).until(
        EC.presence_of_element_located((By.CLASS_NAME, "svelte-1r1jv7l"))           # the svg map
        )
    except:
        pass
        #driver.quit()

    try:
        request = driver.wait_for_request(pat, timeout = N)
    except:
        pass
    """


    # Access requests via the `requests` attribute
    """
    for request in driver.requests:
        if request.response:
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type']
            )
    """
    response = driver.requests[0].response
    #body = decode(response.body, response.headers.get('Content-Encoding', 'identity'))



    responses = [request.response for request in driver.requests]
    responses = [request.response for request in driver.requests]
    entries = []
    for resp in responses:
        headers = [hdr for hdr in resp.headers if hdr[0] == 'content-type']
        if headers:
            content_hdrs = [hdr for hdr in headers if hdr[1]=='text/csv']
            if content_hdrs:
                entries.append(resp)


    return True