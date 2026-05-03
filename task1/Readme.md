# Task 1: Asynchronous Multi-threaded Web Scraper

A web scraper built using **Python asyncio**, **Playwright**, and **SQLite3** to track price changes in Amazon electronics products.

---

## Features

-  **Asynchronous Scraping**
  - Uses `asyncio` for non-blocking execution
  - Runs multiple scraping tasks concurrently

- **Concurrent Execution**
  - Implements **4 concurrent scraping tasks**
  - Uses `asyncio.gather()` for efficient task execution

- **Anti-Detection Mechanisms**
  - Rotates **User Agents**
  - have **delays** to mimic human behavior

- **Amazon Electronics Scraping**
  - Targets specific **electronics category**
  - Extracts product details using Playwright selectors

- **Database Integration**
  - Stores scraped data in **SQLite3**
  - Maintains historical price records

- **Price Change Detection**
  - Compares current prices with stored values
  - Detects increases/decreases in product prices

- **CSV Export**
  - Outputs price changes into a structured **CSV file**

- **Scheduled Execution**
  - Runs automatically **every day at 3 AM**

---

## Tech Stack

- **Python 3**
- **asyncio**
- **Playwright**
- **SQLite3**
- **CSV**

---

##  Project Workflow

1. Initialize Playwright browser
2. Create asynchronous scraping tasks
3. Rotate user agents and apply delays
4. Fetch product data from Amazon
5. Store/update data in SQLite database
6. Compare prices with previous records
7. Export detected changes to CSV
8. Schedule daily execution at 3 AM

---

## Scraping Logic

- Uses Playwright’s built-in methods:
  - `query_selector()`
  - `query_selector_all()`

- Extracts:
  - Product id ASIN number
  - Product Name
  - Price
---


## Scheduling

The scraper is configured to run automatically every day at 3:00am:

## Installation

```bash
python -m venv venv

source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install playwright asyncio

playwright install
