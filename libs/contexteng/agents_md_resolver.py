"""
https://agents.md/
"""

import os

from libs.contexteng.folder_or_file_resolver import validate_working_directory


def resolve_agent_md(working_directory: str) -> tuple[str, str] | tuple[None, None]:
    """
        Find the closest AGENTS.md file starting from working directory down to home folder
        Working directory = where fais was called from terminal
        AGENTS.md file can be nested in a ".agents" subfolder too.
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
        agents_md_path = os.path.join(folder, "AGENTS.md")
        nested_agents_md_path = os.path.join(folder, ".agents", "AGENTS.md")
        if os.path.isfile(agents_md_path):
            with open(agents_md_path, "r") as f:
                content = f.read()
            return agents_md_path, content
        if os.path.isfile(nested_agents_md_path):
            with open(nested_agents_md_path, "r") as f:
                content = f.read()
            return nested_agents_md_path, content
        if folder == home_folder or len(folder) < len(home_folder):
            break
        # dirname of a dir is its parent if there is no final slash
        # and abspath does remove the final slash
        folder = os.path.dirname(folder)

    return None, None
