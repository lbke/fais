from os import path
import unittest
from agentevals.trajectory.match import create_trajectory_match_evaluator

from libs.fais import fais


class TestTrajectory(unittest.TestCase):
    def test_approximate_file_name(self):
        assets = path.join(path.dirname(__file__), "./assets/test_trajectory/")
        ref_outputs = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "list_files",
                            "arguments": {
                                "folder_path": assets
                            }
                        }
                    }
                ],
            },
        ]
        evaluator = create_trajectory_match_evaluator(
            trajectory_match_mode="superset"
        )
        outputs = fais(
            ["Ouvre l'exemple de prop commerciale dans le dossier", assets])
        res = evaluator(outputs=outputs,
                        reference_outputs=ref_outputs)
        print(res)
        self.assertTrue(res["score"])
