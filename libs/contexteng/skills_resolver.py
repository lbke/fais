"""
https://agentskills.io/home

Steps:
0. Resolving .skills
1. Discovery = load skills names and descriptions
2. Activation = read full skill depending on user prompt
and inject in conversation (or system prompt)
3. Execution = agent does its thing

If needing to go further with skill,
switch to a LangChain Deep Agent,
that does have built-in advanced skills support
https://docs.langchain.com/oss/python/deepagents/skills

TODO: implement skill loading as a LangChain middleware
to make setup easier
"""

import glob
import os

from langchain.tools import tool
# TODO: No clue how to find docs for this yaml package?
import yaml

from libs.contexteng.folder_or_file_resolver import validate_working_directory

from pydantic import BaseModel, Field
from libs.display.terminal_printer import tp


def resolve_skills_folder(working_directory: str) -> tuple[str, str] | tuple[None, None]:
    """
        Find the closest .agents/skills folder
        - Check if above home folder, early fail otherwise
        - Look for AGENTS.md file in current folder, then below etc. until home folder
        - If found, return its content, else return None
        - Always returns the content of the upmost AGENTS.md file, meaning that nested files will totally override the upport ones without merging. This is the expected behavior currently documented in the standard.
        NOTE : only accepts AGENTS.md with this specific casing, NOT agents.md, Agents.md etc.
        https://agents.md/

        working_directory is usually obtained using os.getcwd() (directory from user standpoint, and not the localization of fais binary)

        Returns the AGENTS.md file path and content
    """
    (wd_abs_path, home_folder) = validate_working_directory(working_directory)
    folder = wd_abs_path
    while True:
        skills_folder_path = os.path.join(folder, ".agents", "skills")
        if os.path.isdir(skills_folder_path):
            return skills_folder_path
        if folder == home_folder or len(folder) < len(home_folder):
            break
        # dirname of a dir is its parent if there is no final slash
        # and abspath does remove the final slash
        folder = os.path.dirname(folder)

    return None, None


class SkillInfo(BaseModel):
    """
    Represents a skill with its name and description
    Data structure ready to be fed to an LLM
    We stick to standard for length limitation and available fields
    https://agentskills.io/home
    """
    name: str = Field(max_length=64)
    description: str = Field(max_length=1024)


def _discover_standard_skills(skills_folder: str) -> list[tuple[SkillInfo, str]]:
    """
    Discovers .agents/skills/skill-name/SKILL.md
    """
    skill_files = glob.glob(os.path.join(skills_folder, "*/SKILL.md"))
    discovered_skills: list[tuple[SkillInfo, str]] = []
    skill_names = set({})
    for skill_file in skill_files:
        with open(skill_file, "r") as f:
            try:
                # NOTE: there is a "skills-ref" tool but it's maintainance status is not clear
                # so we don't use them yet
                # https://github.com/agentskills/agentskills/tree/main/skills-ref
                content = f.read()
                # We suppose a yaml frontmatter
                split = content.split("---")
                if len(split) < 3:
                    raise ValueError(
                        f"Invalid format in {skill_file}, missing frontmatter")
                fm_text = split[1]
                fm = yaml.load(fm_text, Loader=yaml.FullLoader)
                # parse as yaml
                # TODO: parse frontmatter quickly
                name = fm["name"]
                desc = fm["description"]
                if (name in skill_names):
                    # We do not allow duplicate skill names yet
                    # TODO: add folder name as prefix? might still clash if multiple sources of skills
                    raise ValueError(
                        f"Duplicate skill name {name} in file {skill_file}, skill names must be unique")
                skill_info = SkillInfo(name=name, description=desc)
                skill_info = SkillInfo(
                    name=name, description=desc, skill_file_path=skill_file)
                discovered_skills.append((skill_info, skill_file))
            except Exception as e:
                print(f"Error parsing skill file {skill_file}: {e}")
    return discovered_skills


def _discover_loose_skills(skills_folder: str) -> list[tuple[SkillInfo, str]]:
    """
    Discovers .agents/skills/foobar.md

    Currently, we don't parse their frontmatter and rely only on filename + description

    Technically, root md files are not standard,
    yet they are more user friendly in the context of an agent for administrative tasks
    @see https://github.com/agentskills/agentskills/issues/30
    """
    loose_skill_files = glob.glob(os.path.join(skills_folder, "*.md"))
    discovered_skills: list[tuple[SkillInfo, str]] = []
    for skill_file in loose_skill_files:
        with open(skill_file, "r") as f:
            try:
                content = f.read()
                name = os.path.splitext(os.path.basename(skill_file))[0]
                # Description = beginning of file content
                desc = content[0:157] + \
                    "..." if len(content) > 160 else content
                skill_info = SkillInfo(name=name, description=desc)
                # TODO: override skill info with frontmatter parsing if there happens to be a frontmatter
                discovered_skills.append((skill_info, skill_file))
            except Exception as e:
                print(f"Error parsing skill file {skill_file}: {e}")
    return discovered_skills


def discover_skills(skills_folder: str) -> tuple[list[SkillInfo], dict[str, str]]:
    """
    Discover SKILL.md files in the provided skill folder

    Also supports "loose" skills: 
        - located at root
        - skill name = filename without extension
        - skill description = file content (truncated if too long)
        - no frontmatter configuration (may be supported in the future)

    Expects skill names to be unique

    Returns list of skill info for the LLM
     and a map of skill name and location for loading the complete skill content
    """
    (standard_skills, loose_skills) = _discover_standard_skills(
        skills_folder), _discover_loose_skills(skills_folder)
    # Technically this
    skills = [*loose_skills, *standard_skills]
    skills_info = [s[0] for s in skills]
    skills_location = {s[0].name: s[1] for s in skills}
    skill_names = set({s[0].name for s in skills})
    # TODO: we could improve dupes support by adding a prefix to the skill name based on location
    if (len(skill_names) < len(skills)):
        # Find dupes more precisely
        seen = set({})
        for (skill, _) in skills:
            if skill.name in seen:
                tp.print_info(
                    f"Warning: Duplicate skill name found: {skill.name}, skill names must be unique.")
            seen.add(skill.name)
        raise ValueError(
            f"Duplicate skill names found, skill names must be unique.")
    # parse content to extract skill name and description
    return (skills_info, skills_location)


@tool
def load_skills(runtime, skill_names: list[str]) -> list[str]:
    """
    Load requested skills content
    """
    if not runtime.context.get("skills_location"):
        return "No skills_location map found in agent context, can't load skills"
    skills = []
    for name in skill_names:
        if name not in runtime.context.get("skills_location", {}):
            return f"Skill {name} not found"
        skill_file = runtime.context.get("skills_location")[name]
        with open(skill_file, "r") as f:
            content = f.read()
            skills.append(content)
    return skills
