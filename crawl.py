from urllib.parse import urlsplit


def normalize_url(raw: str) -> str:

    o = urlsplit(raw)

    normalized_url = ""

    if o.hostname:
        normalized_url = o.hostname

    if o.port and not (
        (o.scheme == "https" and o.port == 443) or (o.scheme == "http" and o.port == 80)
    ):
        normalized_url = f"{normalized_url}:{o.port}"

    if o.path:
        normalized_url = f"{normalized_url}{o.path.removesuffix('/').lower()}"

    return normalized_url
