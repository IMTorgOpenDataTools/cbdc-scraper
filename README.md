# CBDC Scraper

This application scrapes sites with informational data on Central Bank Digital Currencies and outputs a summary file.



## Install

See the References to selenium and puppet for installation and configuration.



## Sites

Current sites scraped include:

* https://cbdctracker.org/
* https://www.atlanticcouncil.org/cbdctracker/
  - [google docs data update](https://docs.google.com/spreadsheets/d/e/2PACX-1vRvC1JtWY8a2W4b8DLPfnfb9rmhuHBmWO22TvSXXpk25CZTBU9_8f6YtxM9rmBK2YajII5ltDE6ynGZ/pub?gid=0&single=true&output=csv)

Look into `cbdc_scraper/utils.py` to see the exact urls for documents extracted.



## References


### Prepare environment

Method-2 from [this ref](https://www.geeksforgeeks.org/scraping-data-in-network-traffic-using-python/).

Java


```
sudo apt-get install software-properties-common
sudo apt-get install debian-keyring debian-archive-keyring
sudo apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main'
sudo apt install openjdk-8-jdk
/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -version

nano ~/.bashrc
export JAVA_HOME=/home/vscode/.local/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/jre/bin:$PATH


unzip browsermob-proxy-2.1.4-bin.zip

JAVACMD=/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java browsermob-proxy-2.1.4/bin/browsermob-proxy
```

BrowserMob Proxy
```
wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip

```





### Selenium

I was able to get selenium with a chrome driver - headless browser, installed correctly.

* select and download a chromedriver to `.libs/` from site: `https://sites.google.com/chromium.org/driver/`
* unzip and make it executable: `chmod +x chromedriver`
* in code, set the driver location: `browser = webdriver.Chrome(executable_path=r"./libs/chromedriver")` but use absolute path
* install google chrome binary, [reference](https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-debian-10/):
```
cd .libs/
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
google-chrome
```

__References__

* [promising shell script that may install everything](https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5)


### Pyppeteer

The scraper uses puppeteer which is a headless browser running on NodeJs.  Pyppeteer is the python wrapper for this.

This infrastructure is dependency-heavy, so take care for the following:

* use a container with more dependencies installed, such as Ubuntu, preferably including NodeJs and Python
* update the repositories list: `sudo apt-get update`
* NodeJs can be added if it is not already on you system:
```
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
```
* install dependencies which may not be included: `sudo apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget`
* run in the project root directory: `npm i puppeteer --save`
* run `pyppeteer-install` command in a repl to install the chrome binary, prior to using this library
* ensure code includes: `browser=await launch(options={'args': ['--no-sandbox']})`

__References__

* [good installation post](https://www.toptal.com/puppeteer/headless-browser-puppeteer-tutorial)
* [good reference](https://stackoverflow.com/questions/57217924/pyppeteer-errors-browsererror-browser-closed-unexpectedly)
* [post](https://www.howtogeek.com/devops/how-to-run-puppeteer-and-headless-chrome-in-a-docker-container/)
* [issues](https://github.com/pyppeteer/pyppeteer/issues/194)