# CBDC Scraper

This application scrapes sites with informational data on Central Bank Digital Currencies and outputs a summary report file.



## Install

Install the usual way, or use the `requirements.txt`:

```
pipenv install
```

See the References to selenium-wire for installation and configuration.  This is only necessary when using a proxy for obtaining the `docs.google.com` url of atlanticcouncil backend data; otherwise, selenium-wire is not necessary.



## Usage

Main entrypoint to the program:

```
pipenv run python cbdc_scraper/scraper.py
```


## Sites

Current sites scraped include:

* https://cbdctracker.org/
* https://www.atlanticcouncil.org/cbdctracker/
  - [google docs: backend update](https://docs.google.com/spreadsheets/d/e/2PACX-1vQh27kpYjCRmNoWa4FEpWqLSxLLaqK_hlgqP6wGQLp8Pum7guAYS6i0qt6wIRAPvb5Up6-6wvmTN05s/pub?gid=0&single=true&output=csv)
  - [google docs: github url](https://docs.google.com/spreadsheets/d/e/2PACX-1vRvC1JtWY8a2W4b8DLPfnfb9rmhuHBmWO22TvSXXpk25CZTBU9_8f6YtxM9rmBK2YajII5ltDE6ynGZ/pub?gid=0&single=true&output=csv) which is obtained from [github commit](https://github.com/GeoEcon/cbdc-tracker-svelte/commit/440f83936facad3602c36519b6f1390025e836e8)

Look into `cbdc_scraper/utils.py` to see the exact urls for documents extracted.



## References

### Selenium-wire

Steps to get selenium-wire with a chrome driver - headless browser, installed correctly.

* select and download a chromedriver to `.libs/` from site: `https://sites.google.com/chromium.org/driver/`
* unzip and make it executable: `chmod +x chromedriver`
* in code, set the driver location: `chrome_driver = "./.libs/chromedriver"` but use absolute path
* install google chrome binary, [reference](https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-debian-10/):
```
cd .libs/
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
google-chrome
```
* ensure the driver and binary are of the same version