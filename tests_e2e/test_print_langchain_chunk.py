import io
import unittest

from langchain.messages import AIMessage, ToolMessage
from rich.console import Console

import libs.ui.print_langchain_chunk as print_langchain_chunk


class TestPrintLangchainChunk(unittest.TestCase):
    def test_print_chunk_with_model_and_tool_messages(self):
        model_tool_call_chunk = {
            "model": {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[
                            {
                                "name": "list_files",
                                "args": {"folder_path": "./"},
                                "id": "PXgEU7Wrd",
                                "type": "tool_call",
                            }
                        ],
                    )
                ]
            }
        }
        tool_result_chunk = {
            "tools": {
                "messages": [
                    ToolMessage(
                        content='["./test_e2e.sh", "./install-dev.sh", "./langgraph.json"]',
                        name="list_files",
                        tool_call_id="PXgEU7Wrd",
                    )
                ]
            }
        }
        model_final_text_chunk = {
            "model": {
                "messages": [
                    AIMessage(
                        content=(
                            "Voici les 2 premiers fichiers de ce dossier :\n\n"
                            "1. **test_e2e.sh**\n"
                            "2. **install-dev.sh**\n\n"
                            "À votre service mon cher."
                        )
                    )
                ]
            }
        }

        output = io.StringIO()
        old_console = print_langchain_chunk.console
        old_final_console = print_langchain_chunk.final_console
        try:
            print_langchain_chunk.console = Console(
                file=output,
                force_terminal=False,
                color_system=None,
            )
            print_langchain_chunk.final_console = Console(
                file=output,
                force_terminal=False,
                color_system=None,
            )

            print_langchain_chunk.print_chunk(model_tool_call_chunk)
            print_langchain_chunk.print_chunk(tool_result_chunk)
            print_langchain_chunk.print_chunk(model_final_text_chunk)
        finally:
            print_langchain_chunk.console = old_console
            print_langchain_chunk.final_console = old_final_console

        printed = output.getvalue()
        self.assertIn("Tool call: list_files (id: PXgEU7Wrd)", printed)
        self.assertIn("Tool result for: list_files (id: PXgEU7Wrd)", printed)
        self.assertIn("Result:", printed)
        self.assertIn("Voici les 2 premiers fichiers de ce dossier", printed)
