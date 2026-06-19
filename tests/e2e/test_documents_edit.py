from os import path
import unittest

from openevals import create_trajectory_match_evaluator
from libs.fais import fais
from libs.tools.documents import edit_xml_file_content
from libs.utils import xmlzip


class TestFais(unittest.TestCase):
    def test_changefile(self):
        fixture = path.join(path.dirname(__file__), "./assets/champ.docx")
        print(fixture)
        fixturecopy = path.join(path.dirname(__file__),
                                "./assets/champ_copy.docx")
        outputs = fais(["Remplace [[champ]] par 'valeur'", fixture])
        updatedcontent = xmlzip.extract_content_xml_from_zip(
            fixturecopy).decode("utf-8")
        # Validate result
        self.assertTrue(updatedcontent.find("valeur") > -1)
        self.assertTrue(updatedcontent.find("[[champ]]") == -1)
        # Validate trajectory
        ref_outputs = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "open_xml_file_for_edit",
                            # Leave emtpy and disable argument check in evaluator
                            # Makes the test less brittle
                            "arguments": {}
                        }
                    },
                    {
                        "function": {
                            "name": "edit_xml_file_content",
                            "arguments": {}
                        }
                    }
                ],
            },
        ]
        evaluator = create_trajectory_match_evaluator(
            trajectory_match_mode="superset",
            tool_args_match_mode="ignore"
        )
        res = evaluator(outputs=outputs,
                        reference_outputs=ref_outputs)
        self.assertTrue(res["score"])
