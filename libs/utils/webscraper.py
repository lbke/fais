from urllib import parse

from html_to_markdown import ConversionOptions, convert
import requests

# TODO: extract from agent config later on
DOMAIN_WHITELIST = {"www.lbke.fr"}


class InvalidUrl(Exception):
    pass


class ForbiddenDomain(Exception):
    pass


def assert_valid_url(url: str):
    parsed_url = parse.urlparse(url)
    if not parsed_url.scheme == "https":
        raise InvalidUrl(
            "Expected https url scheme, got {parsed_url.schema} for {url}")
    if not parsed_url.hostname in DOMAIN_WHITELIST:
        raise ForbiddenDomain(
            f"Only whitelisted domains are allowed (no support for wildcard domain yet), got: {parsed_url.hostname}")
    return True


class RequestFailed(Exception):
    pass


def get_html_content(url):
    # requests is recomended over url.openurl
    # https://docs.python.org/3/library/urllib.request.html
    assert_valid_url(url)
    res = requests.get(url)
    if not res.ok:
        raise RequestFailed(f"Request for {url} failed")
    return res.text


def html_to_md(html):
    # TODO: check mime type, improve implementation
    # Python built-in HTML parser could be enough for basic extraction
    # if this dependency ever falls short
    opt = ConversionOptions(
        extract_images=False,
        extract_metadata=False
    )
    md = convert(html, opt)
    return md["content"]
