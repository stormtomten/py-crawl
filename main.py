import sys

from crawl import crawl_page


def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    base_url = sys.argv[1]

    print(f"starting crawl of: {base_url}")
    result = crawl_page(base_url)
    print(f"Number of pages crawled: {len(result)}")
    for url, page in result.items():
        print(f"\n{url}")
        print(f"\theading: {page['heading']}")
        print(f"\tfirst paragraph: {page['first_paragraph']}")
        print(
            f"\tnumber of links: {len(page['outgoing_links'])}, number of images: {len(page['image_urls'])}"
        )


if __name__ == "__main__":
    main()
