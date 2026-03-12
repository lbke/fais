from langchain.tools import tool

from libs.utils.filewalker import walk_folder, list_folder_files


@tool
def list_subfolders(folder_path: str) -> list[str]:
    """
    Explore a folder to list its subfolders.
    Returns a list of directories (without files)

    If no folder is explicitely provided, assume "./" as the starting point
    (current execution folder)
    It is expected to call this function multiple times to find a specific folder,
    depending on the user request.
    If you need to explore a specific folder, call this tool again with a nested folder_path.
    To read the files for a folder, use `list_files` tool.
    """
    folders = walk_folder(folder_path, max_depth=3)
    return folders


@tool
def list_files(folder_path: str) -> str:
    """
    List the files contained in given folder
    """
    files = list_folder_files(folder_path)
    return files


TOOLS = [list_subfolders, list_files]
