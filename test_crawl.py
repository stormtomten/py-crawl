import unittest

from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_strip_https_scheme(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_strip_scheme_and_query(self):
        input_url = "https://www.blog.boot.dev/path/search?q=none"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev/path/search"
        self.assertEqual(actual, expected)

    def test_strip_scheme_and_empty_query(self):
        input_url = "https://www.blog.boot.dev/path/search?"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev/path/search"
        self.assertEqual(actual, expected)

    def test_strip_scheme_in_capitals(self):
        input_url = "HTTP://www.blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_weird_but_legal_path(self):
        input_url = "HTTP://www.blog.boot.dev//path//..//to///page"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev//path//..//to///page"
        self.assertEqual(actual, expected)

    def test_normalize_uppercase(self):
        input_url = "HTTP://WWW.BLOG.BOOT.DEV/PATH"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_retain_explicit_http_port(self):
        input_url = "http://www.blog.boot.dev:443/path"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev:443/path"
        self.assertEqual(actual, expected)

    def test_retain_explicit_https_port(self):
        input_url = "https://www.blog.boot.dev:80/path"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev:80/path"
        self.assertEqual(actual, expected)

    def test_strip_explicit_default_http_port(self):
        input_url = "http://www.blog.boot.dev:80/path"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_strip_explicit_default_https_port(self):
        input_url = "https://www.blog.boot.dev:443/path"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_strip_trailing_slash_on_path(self):
        input_url = "https://www.blog.boot.dev:443/path/"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_strip_trailing_slash_on_domain(self):
        input_url = "https://www.blog.boot.dev/"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev"
        self.assertEqual(actual, expected)

    def test_strip_fragment(self):
        input_url = "https://www.blog.boot.dev/lore#windigoes"
        actual = normalize_url(input_url)
        expected = "www.blog.boot.dev/lore"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
