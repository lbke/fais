from os import path
from shutil import copy

from langchain.tools import tool

from libs.utils import xmlzip


@tool
def open_text_file(filepath: str) -> str:
    """
    Open .txt or .md files
    Assumes the file uses utf8 encoding
    Returns the file's text content
    """
    with open(filepath, 'r', encoding="utf-8") as f:
        return f.read()


@tool
def open_document_file(filepath: str) -> str:
    """
    Use to open .docx or .odt documents
    (Microsoft Word, Libre Office files).
    Returns the file's main text content
    Text content is structured in XML
    """
    return xmlzip.extract_content_xml_from_zip(filepath)


@tool
def update_document(filepath: str, newcontent: str) -> str:
    """
    Updates a document
    This will never actually update the document,
    in order to avoid data loss,
    but instead generate an updated copy of the document
    Returns the new document path if succesful
    """
    filename, ext = path.splitext(filepath)
    copyfilepath = f"{filename}_copy{ext}"
    copy(filepath, copyfilepath)
    xmlzip.update_zip_inner_file(copyfilepath, newcontent)
    return copyfilepath
