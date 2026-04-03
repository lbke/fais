from os import path
import unittest
from libs.contexteng.agents_md_resolver import resolve_agent_md

assets_abs = path.join(path.dirname(__file__), "./assets")


class TestAgentsMd(unittest.TestCase):
    def test_resolve_agent_md(self):
        from libs.contexteng.agents_md_resolver import resolve_agent_md
        agent_md_path, agent_md_content = resolve_agent_md(assets_abs)
        self.assertIsNotNone(agent_md_path)
        self.assertIsNotNone(agent_md_content)
        self.assertEqual(agent_md_content, "root_agents_md_content")

    def test_resolve_agent_nested_md(self):
        agent_md_path, agent_md_content = resolve_agent_md(
            path.join(assets_abs, "nested_agents_md"))
        self.assertIsNotNone(agent_md_path)
        self.assertIsNotNone(agent_md_content)
        self.assertEqual(agent_md_content, "nested_agents_md_content")
        # self.assertEqual(agent_md_content, "nested_agents_md")

    def test_resolve_agent_wrong(self):
        with self.assertRaises(ValueError):
            resolve_agent_md(
                "/etc/passwords")
