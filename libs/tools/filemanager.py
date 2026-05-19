
from shutil import copy

from langchain.tools import tool


@tool
def copy_file(filepath: str, new_directory_or_filepath: str):
    """
    Copy a file to a new location
    The new path can be a directory, in which case the new file has the same name as the previous one
    The new path can also be a file, in which case the new file has a different name
    Use this tool to create new files from a template
    """
    copy(filepath, new_directory_or_filepath)
    return f"Success: copied {filepath} to {new_directory_or_filepath}"


TOOLS = [copy_file]
