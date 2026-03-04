from langchain.tools import tool

from libs.utils.filewalker import walk_folder, list_folder_files


@tool
def explore_folders(folder_path:str)->list[str]:
    """
    Explore a folder, recursively.
    If no folder is explicitely provided, assume "./" as the starting point
    (current execution folder)
    It is expected to call this function multiple times to find a specific file,
    depending on the user request.
    If you need to explore a specific folder, call this tool again with one of the folder listed, or call "list_files" tool for reading files of a specific folder.
    Returns a list of directories (without files)
    """
    folders = walk_folder(folder_path, max_depth=3)
    return folders


@tool
def list_files(folder_path:str)->str:
    """
    List the files of a specific folder
    """
    files=list_folder_files(folder_path)
    return files


TOOLS=[explore_folders, list_files]