import os
from os.path import join, getsize

EXCLUDED_FOLDERS = {"__pycache__", "node_modules"}
MAX_LENGTH = 100


def walk_folder(folder_path: str, max_depth: int = None)->list[str]:
    all_dirs = []
    # We favour relative path for now
    # folder_path = os.path.abspath(folder_path)

    for root, dirs, files in os.walk(folder_path):
        # Calculate current depth
        current_depth = root[len(folder_path):].count(os.sep)

        # If max_depth is set and we've reached it, stop going deeper
        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []  # Clear dirs to prevent going deeper
            continue

        # Filter out hidden and cache directories
        dirs[:] = [d for d in dirs if not d.startswith(
            ".") and d not in EXCLUDED_FOLDERS]

        all_dirs.extend([join(root, dir) for dir in dirs])
        # TODO : add pagination
        if len(all_dirs) > MAX_LENGTH:
            break
    print(all_dirs)
    return all_dirs


def list_folder_files(folder_path: str)->list[str]:
    files = []
    with os.scandir(folder_path) as it:
        for entry in it:
            if entry.is_file() and not entry.name.startswith('.'):
                files.append(join(folder_path,entry.path))
    return files
