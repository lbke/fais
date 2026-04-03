import unittest

from libs.tools.thunderbird import compose_draft_email_thunderbird


class TestThunderbirdTools(unittest.TestCase):
    @unittest.skip("This test opens Thunderbird, not ideal for automated testing")
    def test_draft(self):
        res = compose_draft_email_thunderbird.func({"subject": "hello"})
        self.assertEqual(res, 0)
