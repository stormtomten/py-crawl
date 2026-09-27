from urllib.parse import urlsplit

import requests

from extract_data import PageData, extract_page_data


def normalize_url(raw: str) -> str:
    parsed_url = urlsplit(raw)
    normalized_url = ""
    if parsed_url.hostname:
        normalized_url = parsed_url.hostname
    if parsed_url.port and not (
        (parsed_url.scheme == "https" and parsed_url.port == 443)
        or (parsed_url.scheme == "http" and parsed_url.port == 80)
    ):
        normalized_url = f"{normalized_url}:{parsed_url.port}"

    if parsed_url.path:
        normalized_url = f"{normalized_url}{parsed_url.path.removesuffix('/').lower()}"

    return normalized_url


def get_html(url: str) -> str:
    try:
        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except requests.RequestException as e:
        raise requests.RequestException(f"network error while fetching {url}: {e}")
    if response.status_code >= 400:
        raise ValueError(
            f"response status code: {response.status_code} {response.reason}"
        )
    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise ValueError(f"got non-HTML response: {content_type}")

    return response.text


def crawl_page(
    base_url: str,
    current_url: str | None = None,
    page_data: dict[str, PageData] | None = None,
) -> dict[str, PageData] | None:
    if not current_url:
        current_url = base_url

    parsed_current = urlsplit(current_url)
    parsed_base = urlsplit(base_url)
    if parsed_current.netloc != parsed_base.netloc:
        return

    normalized_current = normalize_url(current_url)

    if not page_data:
        page_data = {}
    if page_data.get(normalized_current):
        return

    print(f"Crawling: {normalized_current}")
    try:
        html = get_html(current_url)
    except (ValueError, requests.RequestException) as e:
        print(f"skipping {current_url}: {e}")
        return

    current_page = extract_page_data(html, current_url)
    page_data[normalized_current] = current_page

    for link in current_page["outgoing_links"]:
        crawl_page(base_url=base_url, current_url=link, page_data=page_data)

    return page_data
