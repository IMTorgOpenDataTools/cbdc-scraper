
import os
from pathlib import Path 
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from browsermobproxy import Server

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

# Enable Performance Logging of Chrome.
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
desired_capabilities['acceptSslCerts'] = True
desired_capabilities['acceptInsecureCerts'] = True




def check_java_available():
  import subprocess, os
  my_env = os.environ.copy()
  my_env['JAVA_HOME'] = Path('/home/vscode/.local/lib/jvm/java-8-openjdk-amd64').absolute().__str__()
  my_env['PATH'] += ':' + Path('/home/vscode/.local/lib/jvm/java-8-openjdk-amd64/bin').absolute().__str__()

  bashCommand = "java -version"
  result = subprocess.run(bashCommand.split(), capture_output=True, text=True, env=my_env)
  result.stderr
  return len(result.stderr) == 152


def set_env_var():
  import os
  os.environ['JAVA_HOME'] = Path('/home/vscode/.local/lib/jvm/java-8-openjdk-amd64').absolute().__str__()
  os.environ['PATH'] += ':' + Path('/home/vscode/.local/lib/jvm/java-8-openjdk-amd64/bin').absolute().__str__()





#url = "https://www.google.com"
url = "https://www.atlanticcouncil.org/cbdctracker/" 
check_java_available()
set_env_var()

path_to_browsermobproxy = Path("./.libs/browsermob-proxy-2.1.4/bin/browsermob-proxy").absolute().__str__()
server = Server(path_to_browsermobproxy, options={'port': 8090})
server.start()
proxy = server.create_proxy(params={"trustAllServers": "true"})
#hostIp = "localhost"
proxy.new_har(url, options={'captureContent': True,
                            'captureHeaders': True,
                            'captureBinaryContent': True
                            })
proxy.wait_for_traffic_to_stop(quiet_period=500, timeout=1000)

chrome_options.add_argument(f"--proxy-server={proxy.proxy}")        #<<< KEY


def selenium_scrape():
    chrome_driver = "./.libs/chromedriver"
    path_driver = Path(chrome_driver).absolute().__str__()
    with webdriver.Chrome(path_driver, 
                          chrome_options=chrome_options, 
                          desired_capabilities=desired_capabilities) as driver:
      driver.get(url)
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(5)

      # Write it to a HAR file.
      with open("network_log1.har", "w", encoding="utf-8") as f:
        f.write(json.dumps(proxy.har))
    
    server.stop()
    return True