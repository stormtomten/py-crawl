import asyncio
from urllib.parse import urlsplit

import aiohttp

from crawl import normalize_url
from extract_data import PageData, extract_page_data


class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int = 3, max_pages: int = 10):
        self.base_url: str = base_url
        self.base_domain: str = urlsplit(base_url).netloc.lower()
        self.page_data: dict[str, PageData] = {}
        self.visited: set[str] = set()
        self.lock = asyncio.Lock()
        self.max_concurrency: int = max_concurrency
        self.max_pages: int = max_pages
        self.all_tasks: set[asyncio.Task[None]] = set()
        self.should_stop: bool = False
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session is None:
            raise RuntimeError(
                "AsyncCrawler session is not open; use 'async with AsyncCrawler(...)'"
            )
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False
            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True

    async def get_html(self, url: str) -> str:
        if self.session is None:
            raise RuntimeError(
                "AsyncCrawler session is not open; use 'async with AsyncCrawler(...)'"
            )

        async with self.session.get(
            url, headers={"User-Agent": "BootCrawler/1.0"}
        ) as response:
            if response.status >= 400:
                raise ValueError(
                    f"response status code: {response.status} {response.reason}"
                )
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                raise ValueError(f"got non-HTML response: {content_type}")

            return await response.text(errors="replace")

    async def crawl_page(
        self,
        current_url: str | None = None,
    ) -> None:
        async with self.lock:
            if self.should_stop:
                return
        if not current_url:
            current_url = self.base_url

        parsed_current = urlsplit(current_url)
        if parsed_current.netloc.lower() != self.base_domain:
            return

        normalized_current = normalize_url(current_url)
        if not await self.add_page_visit(normalized_current):
            return

        async with self.semaphore:
            print(f"Crawling: {normalized_current}")
            try:
                html = await self.get_html(current_url)
                current_page = extract_page_data(html, current_url)
            except Exception as e:  # noqa: BLE001
                print(f"skipping {current_url}: {type(e).__name__}: {e}")
                return

        async with self.lock:
            self.page_data[normalized_current] = current_page

        new_tasks = [
            asyncio.create_task(self.crawl_page(link))
            for link in current_page["outgoing_links"]
        ]
        self.all_tasks.update(new_tasks)
        try:
            results = await asyncio.gather(*new_tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    print(
                        f"error crawling link from {current_url}: {type(result).__name__}: {result}"
                    )
        finally:
            self.all_tasks.difference_update(new_tasks)

    async def crawl(self) -> dict[str, PageData]:
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(
    base_url: str, max_concurrency: int = 3, max_pages: int = 10
) -> dict[str, PageData]:
    async with AsyncCrawler(
        base_url=base_url, max_concurrency=max_concurrency, max_pages=max_pages
    ) as crawler:
        return await crawler.crawl()
