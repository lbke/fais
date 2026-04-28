import traceback

from langchain.tools import tool

from libs.utils.webscraper import ForbiddenDomain, InvalidUrl, RequestFailed, assert_valid_url, get_html_content, html_to_md


@tool
def fetch_web_page_text_content(url: str) -> str:
    """
    Get a web page text content

    Never invent the url, it should always come from the user's inputs
    """
    try:
        assert_valid_url(url)
        content = get_html_content(url)
        md = html_to_md(content)
        return md
    except (InvalidUrl, ForbiddenDomain) as err:
        return str(err)
    except RequestFailed as err:
        traceback.print_exception(err)
        return str(err)


TOOLS = [fetch_web_page_text_content]
