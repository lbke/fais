"""
https://agents.md/
"""

import os


def resolve_agent_md(working_directory: str) -> tuple[str, str] | tuple[None, None]:
    """
        Find the closest AGENTS.md file starting from working directory
        (where fais was called from terminal)
        - Check if above home folder, early fail otherwise
        - Look for AGENTS.md file in current folder, then below etc. until home folder
        - If found, return its content, else return None
        - Always returns the content of the upmost AGENTS.md file, meaning that nested files will totally override the upport ones without merging. This is the expected behavior currently documented in the standard.
        NOTE : only accepts AGENTS.md with this specific casing, NOT agents.md, Agents.md etc.
        https://agents.md/

        working_directory is usually obtained using os.getcwd() (directory from user standpoint, and not the localization of fais binary)

        Returns the AGENTS.md file path and content
    """
    # Not a dir
    if not os.path.isdir(working_directory):
        raise ValueError(f"{working_directory} is not a valid directory")
    # Be above home
    # TODO: reliability to be double checked
    tilde = "~"
    home_folder = os.path.expanduser(tilde)
    if home_folder == tilde:
        raise ValueError(
            "Home folder is not defined, cannot resolve AGENTS.md")
    abs_current_folder = os.path.abspath(working_directory)
    if not abs_current_folder.startswith(home_folder):
        raise ValueError(
            "Current folder is above home folder, cannot resolve AGENTS.md")

    folder = abs_current_folder
    while True:
        agents_md_path = os.path.join(folder, "AGENTS.md")
        if os.path.isfile(agents_md_path):
            with open(agents_md_path, "r") as f:
                content = f.read()
            return agents_md_path, content
        if folder == home_folder or len(folder) < len(home_folder):
            break
        # dirname of a dir is its parent if there is no final slash
        # and abspath does remove the final slash
        folder = os.path.dirname(folder)

    return None, None
