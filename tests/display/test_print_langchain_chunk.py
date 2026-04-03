import unittest

from langchain.messages import AIMessage, ToolMessage

import libs.display.print_langchain_chunk as print_langchain_chunk


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
        print("\n*****Testing print_chunk with model and tool messages:\n")
        print_langchain_chunk.print_chunk(model_tool_call_chunk)
        print_langchain_chunk.print_chunk(tool_result_chunk)
        print_langchain_chunk.print_chunk(model_final_text_chunk)
