import argparse
import asyncio
import sys

from async_crawler import crawl_site_async


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", type=str)
    parser.add_argument("max_concurrency", type=int, nargs="?", default=3)
    parser.add_argument("max_pages", type=int, nargs="?", default=10)
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
    for page in result.values():
        print(f"\n{page['url']}")
        print(f"\theading: {page['heading']}")
        print(f"\tfirst paragraph: {page['first_paragraph']}")
        print(
            f"\tnumber of links: {len(page['outgoing_links'])}, number of images: {len(page['image_urls'])}"
        )


if __name__ == "__main__":
    asyncio.run(main())
