import os
import tempfile
import unittest

from libs.cli.parse_args import parse_args


class TestParseArgs(unittest.TestCase):
    def test_no_prompt_exits(self):
        # argparse itself exits with code 2 when the required 'prompt' argument is missing
        with self.assertRaises(SystemExit) as ctx:
            parse_args([])
        self.assertEqual(ctx.exception.code, 2)

    def test_prompt_too_big_exits(self):
        big_prompt = "a" * 10001
        with self.assertRaises(SystemExit) as ctx:
            parse_args([big_prompt])
        self.assertEqual(ctx.exception.code, 1)

    def test_valid_prompt_no_files(self):
        result = parse_args(["hello world"])
        self.assertEqual(result["prompt"], "hello world")
        self.assertIsNone(result["files"])

    def test_valid_prompt_with_existing_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        try:
            result = parse_args(["hello", tmp_path])
            self.assertEqual(result["prompt"], "hello")
            self.assertEqual(result["files"], [tmp_path])
        finally:
            os.unlink(tmp_path)

    def test_nonexistent_file_raises(self):
        with self.assertRaises(ValueError, msg="File doesn't exist"):
            parse_args(["hello", "/nonexistent/path/file.txt"])

    def test_prompt_at_max_length(self):
        max_prompt = "a" * 10000
        result = parse_args([max_prompt])
        self.assertEqual(result["prompt"], max_prompt)
        self.assertIsNone(result["files"])
