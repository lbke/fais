from zipfile import ZipFile
import os
from os import path
from shutil import copyfile, move
import tempfile


def _assert_supported_filetype(file_path: str):
    filename, extension = path.splitext(file_path)
    if not extension in {".docx", ".odt"}:
        raise Exception(
            f"Unsupported file type '{extension}' for file '{file_path}'")


def _get_zip_content_file_name(file_path: str) -> str:
    """
    docx and odt are both zipped archive containing multiple XML files
    => we aim for the content file for variable injection
    Run ZipFile.printdir() to check the content of a file
    """
    _assert_supported_filetype(file_path)
    filename, extension = path.splitext(file_path)
    match extension:
        case ".docx":
            return "word/document.xml"
        case ".odt":
            return "content.xml"


def extract_xml_from_zip(file_path: str) -> str:
    """
    .odt, .docx and maybe other formats are simply zipped XML
    """
    try:
        with ZipFile(file_path, 'r') as zf:
            # print(zf.printdir())
            # Read content.xml from the ODT file
            content_file = _get_zip_content_file_name(file_path)
            content_xml = zf.read(content_file).decode('utf-8')
            return content_xml
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from ODT: {str(e)}")

# NOTE: it's not possible to update the content of a single zip file
# as any change will affect the zip structure, index, offset
# => zip file must be rebuilt systematically


def _update_zip_inner_file(zip_path, target_filename, new_content):
    # Create a temporary ZIP file
    fd, temp_zip_path = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    with ZipFile(zip_path, 'r') as zin:
        with ZipFile(temp_zip_path, 'w') as zout:
            for item in zin.infolist():
                if item.filename == target_filename:
                    # Replace the file with new content
                    zout.writestr(item, new_content)
                else:
                    # Copy original file unchanged
                    zout.writestr(item, zin.read(item.filename))
    # Replace original archive
    move(temp_zip_path, zip_path)


def main():
    print("Hello from docx-updater!")
    # NOTE: this may lose permissions
    # @see https://docs.python.org/3/library/shutil.html
    file_path = "./test.docx"
    filename, ext = path.splitext(file_path)
    copy_file_path = f"{filename}_copy{ext}"
    copyfile(file_path, copy_file_path)
    content = extract_xml_from_zip(copy_file_path)
    print("Finding [[champ]]:", content.find("[[champ]]"))
    new_content = content.replace("[[champ]]", "valeur_champ")
    _update_zip_inner_file(
        copy_file_path, _get_zip_content_file_name(copy_file_path), new_content)


if __name__ == "__main__":
    main()
