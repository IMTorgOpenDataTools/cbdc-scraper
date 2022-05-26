import asyncio
from pyppeteer import launch

url_csv = "https://doc-08-0k-sheets.googleusercontent.com/pub/70cmver1f290kjsnpar5ku2h9g/tkn2b49778hu2oba4aigcnaato/1653582840000/106914790471774643264/*/e@2PACX-1vQh27kpYjCRmNoWa4FEpWqLSxLLaqK_hlgqP6wGQLp8Pum7guAYS6i0qt6wIRAPvb5Up6-6wvmTN05s?gid=0&single=true&output=csv"

async def new_scrape():
    # launch chromium browser in the background
    browser = await launch(options={'args': ['--no-sandbox']})
    #browser = await launch()
    # open a new tab in the browser
    page = await browser.newPage()
    # add URL to a new page and then open it
    await page.goto("https://www.atlanticcouncil.org/cbdctracker/")
    # create a screenshot of the page and save it
    #await page.screenshot({"path": "python.png"})
    await page.setRequestInterception(True)
    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')
    print(dimensions)
    csv_file = await page.goto(url_csv)
    
    # close the browser
    await browser.close()

def puppet_scrape():
    print("Starting...")
    asyncio.get_event_loop().run_until_complete(new_scrape())
    print("Screenshot has been taken")