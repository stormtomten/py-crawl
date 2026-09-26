from urllib.parse import urlsplit


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
