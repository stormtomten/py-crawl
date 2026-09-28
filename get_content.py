from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    h_tag = soup.find("h1") or soup.find("h2")
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    main = soup.find("main")
    p_tag = main.find("p") if isinstance(main, Tag) else None
    p_tag = p_tag or soup.find("p")

    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    anchors = [tag for tag in soup.find_all("a") if isinstance(tag, Tag)]

    hrefs = [
        href for tag in anchors if isinstance(href := tag.get("href"), str) and href
    ]
    links = [urljoin(base_url, href) for href in hrefs]
    return links


def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    images = [tag for tag in soup.find_all("img") if isinstance(tag, Tag)]

    srcs = [src for tag in images if isinstance(src := tag.get("src"), str) and src]
    image_urls = [urljoin(base_url, src) for src in srcs]

    return image_urls
