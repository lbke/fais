import os


def validate_working_directory(wd: str) -> tuple[str, str] | tuple[None, None]:
    """
        Validate the working directory

        wd working directory relative or absolute path

        working_directory is usually obtained using os.getcwd() (directory from user standpoint, and not the localization of fais binary)

        Returns the working directory absolute path + the home folder path
    """
    # Not a dir
    if not os.path.isdir(wd):
        raise ValueError(f"{wd} is not a valid directory")
    # Working directory must always be above home
    # TODO: reliability to be double checked
    tilde = "~"
    home_folder = os.path.expanduser(tilde)
    if home_folder == tilde:
        raise ValueError(
            "Home folder is not defined")
    abs_current_folder = os.path.abspath(wd)
    if not abs_current_folder.startswith(home_folder):
        raise ValueError(
            f"Working directory {wd} is above home folder, cannot resolve AGENTS.md")

    folder = abs_current_folder
    return folder, home_folder
