import unittest

from langchain.tools import ToolException, tool
from libs.middlewares.handle_file_errors import HandleFileErrorsMiddleware


class TestHandleFileErrors(unittest.TestCase):
    def test_handle_file_errors_middleware(self):

        @tool
        def raise_file_not_found_error_tool():
            """ Dummy tool that raise error"""
            raise FileNotFoundError("fake_path.docx not found")
        # Test NotADirectoryError for list_files_in_folder

        @tool
        def raise_not_a_directory_error_tool():
            """ Dummy tool that raise error"""
            raise NotADirectoryError("fake_folder is not a directory")

        # Test FileNotFoundError for read_document_file_text_content
        with self.assertRaises(ToolException) as err:
            result = HandleFileErrorsMiddleware.wrap_tool_call(
                "fake_path.docx", raise_file_not_found_error_tool.invoke)
        with self.assertRaises(ToolException) as err:
            result = HandleFileErrorsMiddleware.wrap_tool_call(
                "fake_folder", raise_not_a_directory_error_tool.invoke)
