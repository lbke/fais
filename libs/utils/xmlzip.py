import os
from shutil import move
import tempfile

from os import path
from zipfile import BadZipFile, ZipFile

"""
Handles zipped xml file types such as docx, odt
"""


def _assert_supported_filetype(file_path: str):
    """
    Currently supporting docx and zip
    Could be generalized using an adapter pattern
    """
    filename, extension = path.splitext(file_path)
    if not extension in {".docx", ".odt"}:
        raise Exception(
            f"Unsupported file type '{extension}' for file '{file_path}'")


def _get_zip_content_file_name(file_path: str) -> str:
    """
    Get main text content file in docx or odt file
    (currently we don't handle metadata and such)
    """
    _assert_supported_filetype(file_path)
    filename, extension = path.splitext(file_path)
    match extension:
        case ".docx":
            return "word/document.xml"
        case ".odt":
            return "content.xml"


def extract_content_xml_from_zip(file_path: str) -> str:
    """
    Get the main content file XML content

    It's NOT decoded (with utf-8) as the XML file itself contains the encoding information
    """
    try:
        with ZipFile(file_path, 'r') as zf:
            # print(zf.printdir())
            # Read content.xml from the ODT file
            content_file = _get_zip_content_file_name(file_path)
            content_xml = zf.read(content_file)
            # NOTE: we don't decode as encoding is already signalled in the XML file
            # @see https://stackoverflow.com/questions/28534460/lxml-etree-xml-valueerror-for-unicode-string
            # .decode('utf-8')
            return content_xml
    except FileNotFoundError as err:
        # File not found are handled at tool level
        raise err
    except BadZipFile as err:
        raise BadZipFile(
            f"File {file_path} is not a zip file, it can't be opened as such: {str(err)}")
    except Exception as e:
        raise RuntimeError(
            f"Failed to extract text from ODT or DOCX file {file_path}: {type(e)} {str(e)}")

# NOTE: it's not possible to update the content of a single zip file
# as any change will affect the zip structure, index, offset
# => zip file must be rebuilt systematically


def update_zip_inner_file(zip_path, new_content):
    """
    Update a file within a zip archive
    This requires recreating the whole archive
    """
    # Create a temporary ZIP file
    fd, temp_zip_path = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    with ZipFile(zip_path, 'r') as zin:
        with ZipFile(temp_zip_path, 'w') as zout:
            # content.xml for word etc
            target_filename = _get_zip_content_file_name(zip_path)
            for item in zin.infolist():
                if item.filename == target_filename:
                    # Replace the file with new content
                    zout.writestr(item, new_content)
                else:
                    # Copy original file unchanged
                    zout.writestr(item, zin.read(item.filename))
    # Replace original archive
    move(temp_zip_path, zip_path)
