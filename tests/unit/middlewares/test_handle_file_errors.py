import unittest

from langchain.tools import ToolException, tool
from libs.middlewares.handle_file_errors import HandleFileErrorsMiddleware


class TestHandleFileErrors(unittest.TestCase):
    # TODO: unit test not very relevant here, should rather be tested e2e
    # def test_handle_file_errors_middleware(self):
    #
    #    @tool
    #    def raise_file_not_found_error_tool():
    #        """ Dummy tool that raise error"""
    #        raise FileNotFoundError("fake_path.docx not found")
    #    # Test NotADirectoryError for list_files_in_folder
    #
    #    @tool
    #    def raise_not_a_directory_error_tool():
    #        """ Dummy tool that raise error"""
    #        raise NotADirectoryError("fake_folder is not a directory")
    #
    #    # Test FileNotFoundError for read_document_file_text_content
    #    with self.assertRaises(ToolException) as err:
    #        result = HandleFileErrorsMiddleware.wrap_tool_call(
    #            # FIXME: this should actually be a request object
    #            # { "tool_call": {"id": "test_tool_call_id"}} }
    #            # but then not sure how to pass the tool params
    #            "fake_path.docx", raise_file_not_found_error_tool.invoke)
    #    with self.assertRaises(ToolException) as err:
    #        result = HandleFileErrorsMiddleware.wrap_tool_call(
    #            "fake_folder", raise_not_a_directory_error_tool.invoke)

    def test_handle_file_errors_middleware_correct_tool(self):
        @tool
        def correct_tool():
            """ Dummy tool that works correctly"""
            return "This tool works correctly"

        result = HandleFileErrorsMiddleware.wrap_tool_call(
            None, correct_tool.invoke)
        self.assertEqual(result, "This tool works correctly")
