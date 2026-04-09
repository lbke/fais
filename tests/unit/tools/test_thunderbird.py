import unittest

from libs.tools.thunderbird import EmailContent, compose_draft_email_thunderbird, EmailContent


class TestThunderbirdTools(unittest.TestCase):
    @unittest.skip("This test opens Thunderbird, not ideal for automated testing")
    def test_draft(self):
        res = compose_draft_email_thunderbird.func({"subject": "hello"})
        self.assertEqual(res, 0)

    def test_no_attachement(self):
        email_content = EmailContent(
            subject="hello", to="test@test.test", body="world")
        res = email_content.generate_email()
        self.assertFalse("attachment" in res)

    def test_attachement(self):
        email_content = EmailContent(
            subject="hello", to="test@test.test", body="world", attachment=__file__)
        res = email_content.generate_email()
        print(res)
        self.assertTrue(f"attachment='{__file__}'" in res)
