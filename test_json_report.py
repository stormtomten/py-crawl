import json
import os
import tempfile
import unittest

from extract_data import PageData
from json_report import write_json_report


def make_page(url: str) -> PageData:
    return {
        "url": url,
        "heading": f"heading of {url}",
        "first_paragraph": f"paragraph of {url}",
        "outgoing_links": [],
        "image_urls": [],
    }


class TestWriteJsonReport(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def temp_path(self, name: str) -> str:
        return os.path.join(self.temp_dir.name, name)

    def test_writes_valid_json_to_given_filename(self):
        path = self.temp_path("custom.json")
        page_data = {"https://example.com": make_page("https://example.com")}

        write_json_report(page_data, path)

        with open(file=path, mode="r", encoding="utf-8") as file:
            actual = json.load(file)
        self.assertEqual(actual, [page_data["https://example.com"]])

    def test_pages_sorted_by_url(self):
        path = self.temp_path("sorted.json")
        page_data = {
            "https://example.com/c": make_page("https://example.com/c"),
            "https://example.com/a": make_page("https://example.com/a"),
            "https://example.com/b": make_page("https://example.com/b"),
        }

        write_json_report(page_data, path)

        with open(file=path, mode="r", encoding="utf-8") as file:
            actual = json.load(file)
        urls = [page["url"] for page in actual]
        self.assertEqual(
            urls,
            [
                "https://example.com/a",
                "https://example.com/b",
                "https://example.com/c",
            ],
        )

    def test_empty_page_data_writes_empty_list(self):
        path = self.temp_path("empty.json")

        write_json_report({}, path)

        with open(file=path, mode="r", encoding="utf-8") as file:
            actual = json.load(file)
        self.assertEqual(actual, [])

    def test_creates_missing_parent_directory(self):
        path = self.temp_path(os.path.join("nested", "dir", "report.json"))

        write_json_report({}, path)

        self.assertTrue(os.path.exists(path))

    def test_default_filename_is_out_report_json(self):
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        self.addCleanup(os.chdir, original_cwd)

        write_json_report({"https://example.com": make_page("https://example.com")})

        self.assertTrue(os.path.exists(os.path.join("out", "report.json")))


if __name__ == "__main__":
    unittest.main()
