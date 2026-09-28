import asyncio
import sys

from async_crawler import crawl_site_async


async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 3:
        print("too many arguments provided")
        sys.exit(1)
    base_url = sys.argv[1]
    max_concurrency = 5
    if len(sys.argv) == 3:
        try:
            max_concurrency = int(sys.argv[2])
            if max_concurrency < 1:
                raise ValueError
        except ValueError:
            print("max_concurrency must be a positive integer")
            sys.exit(1)

    print(f"starting crawl of: {base_url}")
    result = await crawl_site_async(base_url, max_concurrency)
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
