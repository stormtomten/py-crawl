import argparse
import asyncio
import sys

from async_crawler import crawl_site_async
from json_report import write_json_report


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", type=str)
    parser.add_argument("max_concurrency", type=int, nargs="?", default=3)
    parser.add_argument("max_pages", type=int, nargs="?", default=10)
    parser.add_argument("file_path", type=str, nargs="?", default="out/report.json")
    args = parser.parse_args()
    if args.max_concurrency < 0:
        print("max concurrency must be a positive integer")
        sys.exit(1)
    if args.max_pages < 0:
        print("max pages must be a positive integer")
        sys.exit(1)

    print(f"starting crawl of: {args.base_url}")
    result = await crawl_site_async(args.base_url, args.max_concurrency, args.max_pages)
    print(f"Number of pages crawled: {len(result)}")
    write_json_report(result, args.file_path)


if __name__ == "__main__":
    asyncio.run(main())
