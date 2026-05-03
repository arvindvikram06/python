import argparse
import asyncio
from crawler import WebCrawler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--concurrency", type=int, default=10)

    args = parser.parse_args()

    crawler = WebCrawler(
        seed_url=args.seed,
        max_depth=args.depth,
        concurrency=args.concurrency
    )

    asyncio.run(crawler.run())

if __name__ == "__main__":
    main()