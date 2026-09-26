import sys

from crawl import get_html


def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    base_url = sys.argv[1]

    print(f"starting crawl of: {base_url}")
    result = get_html(base_url)
    print(result)


if __name__ == "__main__":
    main()
