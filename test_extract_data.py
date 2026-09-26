import unittest

from extract_data import extract_page_data


class TestExtractPageData(unittest.TestCase):
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_empty_page(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_main_paragraph_priority_multi_link_image(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <p>This is the first paragraph but outside of main.</p>
            <img src="/image1.jpg" alt="Image 1">
            <main>
            <h1>Test Title</h1>
            <p>This is the second paragraph but the first in main.</p>
            <a href="/link1">Link 1</a>
            <a href="http://outsidelink.com">Link 2</a>
            <img src="/image2.jpg" alt="Image 2">
            </main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the second paragraph but the first in main.",
            "outgoing_links": [
                "https://crawler-test.com/link1",
                "http://outsidelink.com",
            ],
            "image_urls": [
                "https://crawler-test.com/image1.jpg",
                "https://crawler-test.com/image2.jpg",
            ],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_heading_priority(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        <h2>This is the first heading but of lower importance!</h2>
        <h1>This is the second heading but of higher importance!</h1>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "This is the second heading but of higher importance!",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_heading_and_paragraph_fallback(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        <p>First paragraph outside of main.</p>
        <main>
        <h2>This is the first heading fallback!</h2>
        </main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "This is the first heading fallback!",
            "first_paragraph": "First paragraph outside of main.",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
