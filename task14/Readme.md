# Task 14: Asynchronous Multi-threaded Web Crawler

A high-performance web crawler built using **Python asyncio** and **aiohttp** to perform concurrent website exploration, link analysis, and SEO auditing.

---

## Features

- **Asynchronous Concurrency**
  - Uses `asyncio.Semaphore` to limit and manage concurrent HTTP requests.
  - Non-blocking execution for efficient crawling of large sites.

- **Depth-limited Crawling**
  - Configurable crawl depth to control exploration limits.
  - Prevents infinite loops and unnecessary resource consumption.

- **Robots.txt Compliance**
  - Automatically fetches and respects `robots.txt` rules for the target domain.
  - Ensures ethical scraping by skipping disallowed paths.

- **SEO Auditing**
  - Identifies **Broken Links** (404 errors).
  - Detects **Redirect Chains** and loops.
  - Finds **Orphan Pages** (pages with no inbound internal links).

- **Output Generation**
  - Generates a visual graph of the site structure.
  - Automatically produces an XML sitemap of all crawled URLs.

---

## Tech Stack

- **Python 3**
- **Asyncio**
- **aiohttp** (Asynchronous HTTP requests)
- **BeautifulSoup4** (HTML parsing)
- **collections** (deque for URL queueing)

---

## Project Workflow

1. **Initialization**: Provide a seed URL and maximum depth via CLI.
2. **Robots Discovery**: The crawler first checks `robots.txt` for permissions.
3. **Queueing**: The seed URL is added to the asynchronous crawl queue.
4. **Fetching & Parsing**:
   - The fetcher retrieves the page content asynchronously.
   - The parser extracts all internal links from the HTML.
5. **Deduplication**: Checks visited URLs to avoid redundant requests.
6. **Reporting**: After the crawl completes, the system analyzes the results to generate an SEO audit report and structural graph.

---

## Crawling Logic

- **Normalization**: Ensures `https://example.com/` and `https://example.com` are treated as the same URL.
- **Domain Locking**: The crawler stays within the same domain as the seed URL.
- **Error Handling**: Gracefully handles timeouts and connection errors without stopping the entire crawl.

---

## Installation

```bash
pip install aiohttp beautifulsoup4
python main.py --seed https://example.com --depth 3 --concurrency 20
```
