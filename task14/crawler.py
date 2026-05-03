import asyncio
from collections import deque, defaultdict
import aiohttp
import os

from fetcher import fetch
from parser import extract_links
from robots import RobotsHandler
from storage import save_graph, save_sitemap
from utils import normalize_url, same_domain
from reporter import generate_report

class WebCrawler:
    def __init__(self, seed_url, max_depth, concurrency):
        self.seed_url = seed_url
        self.max_depth = max_depth
        self.semaphore = asyncio.Semaphore(concurrency)

        self.queue = deque([(seed_url, 0)])
        self.visited = set()

        self.graph = defaultdict(list)
        self.results = {}
        self.inbound_count = defaultdict(int)

        # metrics
        self.skipped_robots = 0
        self.duplicates = 0

        self.robots = RobotsHandler(seed_url)

        os.makedirs("output", exist_ok=True)

    async def worker(self, session, url, depth):
        async with self.semaphore:

            if url in self.visited:
                self.duplicates += 1
                return

            if not same_domain(self.seed_url, url):
                return

            if not self.robots.allowed(url):
                self.skipped_robots += 1
                return

            self.visited.add(url)

            data = await fetch(session, url)
            self.results[url] = data

            status = data["status"]
            time_taken = data["time"]
            redirects = data["redirects"]

            # logging
            if status == 404:
                print(f"[DEPTH {depth}] {url} 404 NOT FOUND")
            elif redirects:
                print(f"[DEPTH {depth}] {url} {status} -> {data['final_url']}")
            else:
                print(f"[DEPTH {depth}] {url} {status} OK {time_taken}s")

            if data["html"] and depth < self.max_depth:
                links = extract_links(url, data["html"])

                for link in links:
                    norm = normalize_url(link)

                    self.graph[url].append(norm)
                    self.inbound_count[norm] += 1

                    self.queue.append((norm, depth + 1))

    async def run(self):
        print("=== Crawl Started ===")
        print(f"Seed: {self.seed_url}")

        await self.robots.load()

        async with aiohttp.ClientSession() as session:
            while self.queue:
                tasks = []

                for _ in range(len(self.queue)):
                    url, depth = self.queue.popleft()
                    tasks.append(self.worker(session, url, depth))

                await asyncio.gather(*tasks)

        self.final_report()

    def final_report(self):
        broken, redirects, orphan = generate_report(
            self.results, self.inbound_count, self.seed_url
        )

        print("\n=== Crawl Complete ===")
        print(f"Pages crawled: {len(self.visited)}")
        print(f"Unique URLs: {len(self.results)}")
        print(f"Skipped (robots): {self.skipped_robots}")
        print(f"Duplicates avoided: {self.duplicates}")

        print("\n=== SEO Audit ===")

        print("\nBroken Links:")
        for b in broken:
            print(" -", b)

        print("\nRedirect Chains:")
        for k, v in redirects.items():
            if len(v) > 1:
                print(f" - {k} -> {' -> '.join(v)}")

        print("\nOrphan Pages:")
        for o in orphan:
            print(" -", o)

        save_graph(self.graph)
        save_sitemap(self.visited)

        print("\nSaved to /output/")