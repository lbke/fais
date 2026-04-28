import unittest

from libs.utils.webscraper import ForbiddenDomain, get_html_content, html_to_md


class TestWebScraper(unittest.TestCase):
    def test_invalid_domain(self):
        with self.assertRaises(ForbiddenDomain):
            get_html_content("https://pirateworld.com")

    def test_invalid_subdomain(self):
        # We don't currently support wildcard
        # -> subdomains must be whitelisted one at  a time
        with self.assertRaises(ForbiddenDomain):
            get_html_content("https://pirateworld.lbke.fr")

    def test_get_html_content(self):
        content = get_html_content("https://www.lbke.fr/mentions-legales")
        self.assertTrue(content.find("Mentions légales"))

    def test_url_to_html_to_markdown(self):
        content = get_html_content("https://www.lbke.fr/mentions-legales")
        md = html_to_md(content)
        print(md)
        self.assertTrue(md.find("# Mentions légales"))
