from os import path
import unittest

from libs.contexteng.skills_resolver import discover_skills, resolve_skills_folder


assets_abs = path.join(path.dirname(__file__), "./assets")


class TestSkillsMd(unittest.TestCase):
    def test_discover_standard_skill(self):
        skills_folder = path.join(assets_abs, "skills")
        resolved_skills_folder = resolve_skills_folder(skills_folder)

        self.assertIsNotNone(resolved_skills_folder)

        skills_info, skills_location = discover_skills(resolved_skills_folder)

        self.assertIn("standard-skill", skills_location)

        standard_skill = next(
            (skill for skill in skills_info if skill.name == "standard-skill"),
            None,
        )
        self.assertIsNotNone(standard_skill)
        self.assertEqual(standard_skill.description, "Nested")

    def test_discover_loose_skill(self):
        skills_folder = path.join(assets_abs, "skills")
        resolved_skills_folder = resolve_skills_folder(skills_folder)

        self.assertIsNotNone(resolved_skills_folder)

        skills_info, skills_location = discover_skills(resolved_skills_folder)

        self.assertIn("loose-skill", skills_location)

        loose_skill = next(
            (skill for skill in skills_info if skill.name == "loose-skill"),
            None,
        )
        self.assertIsNotNone(loose_skill)
        self.assertEqual(loose_skill.description, "Root skill")
