import unittest

from get_content import (
    get_first_paragraph_from_html,
    get_heading_from_html,
    get_images_from_html,
    get_urls_from_html,
)


class TestGetHeadingFromHTML(unittest.TestCase):
    def test_get_heading_first_heading_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_second_heading_basic(self):
        input_body = "<html><body><h2>Test Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_no_heading(self):
        input_body = "<html><body><p>Test Title</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


class TestGetFirstParagraph(unittest.TestCase):
    def test_get_first_paragraph_main_priority_one_main_paragraph(self):
        input_body = """<html><body>
				<p>Outside paragraph.</p>
				<main>
					<p>Main paragraph.</p>
				</main>
			</body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_main_priority_two_main_paragraphs(self):
        input_body = """"<html><body>
                <p>Outside paragraph.</p>
                <main>
                    <p>First paragraph.</p>
                    <p>Second paragraph.</p>
                </main>
            </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main_paragraph(self):
        input_body = """<html><body>
				<p>Outside paragraph.</p>
				<p>Second paragraph outside main</p>
				<main>
					<h1>Main paragraph.</h1>
				</main>
			</body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_empty_paragraph_fallback(self):
        input_body = """<html><body>
				<p>Outside paragraph.</p>
				<main>
					<p></p>
					<p>Second paragraph.</p>
				</main>
			</body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


class TestGetURLsFromHTML(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com/"
        input_body = (
            '<html><body><a href="/team/about"><span>Boot.dev</span></a></body></html>'
        )
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/team/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_query(self):
        input_url = "https://crawler-test.com/"
        input_body = '<html><body><a href="/search?q=boot#top"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/search?q=boot#top"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_empty_href(self):
        input_url = "https://crawler-test.com/"
        input_body = '<html><body><a href=""><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_missing_href(self):
        input_url = "https://crawler-test.com/"
        input_body = "<html><body><a></a></body></html>"
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_links(self):
        input_url = "https://crawler-test.com/"
        input_body = "<html><body><p>Bulle</p></body></html>"
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_finds_all_and_attribute_not_in_main(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <a href="/first"><b>Boot.dev</b></a>
        <html><body>
        <a href="/second"><span>Boot.dev</span></a>
        <a href="/third"><span>Boot.dev</span></a>
        </body></html>
        """
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/first",
            "https://crawler-test.com/second",
            "https://crawler-test.com/third",
        ]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_other_host(self):
        input_url = "https://crawler-test.com/"
        input_body = '<html><body><a href="https://boot.dev/blog"></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://boot.dev/blog"]
        self.assertEqual(actual, expected)


class TestGetImagesFromHTML(unittest.TestCase):
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_other_host(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://boot.dev/images/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://boot.dev/images/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_finds_all_and_attribute_not_in_main(self):
        input_url = "https://crawler-test.com"
        input_body = """
        <img src="first.png" alt="Logo">
        <html><body><img src="second.png" alt="Logo"></body></html>
        <html><body><img src="third.png" alt="Logo"></body></html>
        """
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/first.png",
            "https://crawler-test.com/second.png",
            "https://crawler-test.com/third.png",
        ]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_no_image(self):
        input_url = "https://crawler-test.com/"
        input_body = "<html><body><p>Bulle</p></body></html>"
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_empty_src(self):
        input_url = "https://crawler-test.com/"
        input_body = '<html><body><img src=""><span>Boot.dev</span></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com/"
        input_body = "<html><body><img></body></html>"
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
