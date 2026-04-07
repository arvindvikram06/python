import asyncio
import re
import random
from datetime import datetime
from playwright.async_api import async_playwright

from db import init_db, save_products, last_seen_prices
from report import generate_report

PAGES = 20
CONCURRENCY = 4

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36"
]

price_regex = re.compile(r"([0-9,]+\.[0-9]{2})") # regex to detect price in an item

async def get_products(page):
    items = await page.query_selector_all("div.s-result-item[data-asin]")  # this fetches the all products from current page
    products = []

    for item in items:
        asin = await item.get_attribute("data-asin")   # each amazon product has a unique (ASIN) identification number  
        title_el = await item.query_selector("h2 span") # selects title item
        text = await item.inner_text() # extract the inner text of full product
        match = price_regex.search(text) # searches whether a text matches the price regex

        if not asin or not title_el or not match: #skips the product if any one field is missing
            continue

        title = await title_el.inner_text()
        price = float(match.group(1).replace(",", ""))

        products.append((asin, title, price, datetime.now().isoformat()))  

    return products

async def scrape_page(context, page_no):
    page = await context.new_page()

    url = f"https://www.amazon.com/s?k=electronics&page={page_no}"

    print(f"[{datetime.now()}] Opening {url}")

    await page.goto(url, timeout=60000) # added waiting time for loading url
    await page.wait_for_timeout(5000) # provided this delay for the js rendered products to load

    products = await get_products(page)

    print(f"Page {page_no} — {len(products)} products")

    await page.close()
    return products

async def main():
    init_db()
    old = last_seen_prices()

    all_products = []
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(   
            user_agent=random.choice(USER_AGENTS), #rotating the user agent in the header to mimic
            viewport={"width": 1280, "height": 800}
        )

        await context.set_extra_http_headers({
            "accept-language": "en-US,en;q=0.9"
        })

        async def sem_task(page_no): # this function returns a coroutine object
            await semaphore.acquire()
            try:
                return await scrape_page(context, page_no)
            finally:
                semaphore.release()

        tasks = []

        for i in range(1, PAGES + 1):
            task = sem_task(i)  
            tasks.append(task) # first we append all the task object(coroutine)

        results = await asyncio.gather(*tasks) # this executes the tasks we added concurrently with limit 4 at a time

        for res in results:
            all_products.extend(res)

        await context.close()
        await browser.close()

    save_products(all_products)

    changes = []

    for asin, title, price, _ in all_products:
        if asin in old and old[asin] != price:
            changes.append([title, old[asin], price])  # we detect the price change

    generate_report(changes) # generate the report

    print(f"\nTotal products fetched: {len(all_products)}")

if __name__ == "__main__":
    asyncio.run(main())