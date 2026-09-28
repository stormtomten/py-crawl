import json
import os

from extract_data import PageData


def write_json_report(
    page_data: dict[str, PageData], filename: str = "out/report.json"
):
    pages = sorted(page_data.values(), key=lambda p: p["url"])

    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(file=filename, mode="w", encoding="utf-8") as file:
        json.dump(pages, file, indent=2)
