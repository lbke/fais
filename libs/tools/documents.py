from os import path
from shutil import copy

from langchain.tools import tool

from libs.utils import xmlzip
from xml.etree import ElementTree


@tool
def copy_file(filepath: str, new_directory_or_filepath: str):
    """
    Copy a file to a new location
    The new path can be a directory, in which case the new file has the same name as the previous one
    The new path can also be a file, in which case the new file has a different name
    Use this tool to create new files from a template
    """
    copy(filepath, new_directory_or_filepath)


@tool
def open_document_file_as_xml(filepath: str) -> str:
    """
    Use to open .docx or .odt documents
    (Microsoft Word, Libre Office files).
    Returns the file's main text content, structured in XML
    The XML can be edited to create a new file, as long as the structure is respected.
    """
    return xmlzip.extract_content_xml_from_zip(filepath)


@tool
def read_text_file(filepath: str) -> str:
    """
    Open .txt or .md files
    Assumes the file uses utf8 encoding
    Returns the file's text content
    """
    with open(filepath, 'r', encoding="utf-8") as f:
        return f.read()


@tool
def read_document_file_text_content(filepath: str) -> str:
    """
    Use to open .docx or .odt documents
    (Microsoft Word, Libre Office files).
    Returns the file's main text content, in pure text
    This function loses the XML structure of the document (not suited for later updates)
    """
    xml = xmlzip.extract_content_xml_from_zip(filepath)
    root = ElementTree.fromstring(xml)
    text_chunks = [chunk.strip() for chunk in root.itertext() if chunk and chunk.strip()]
    return " ".join(text_chunks)


@tool
def update_document_with_xml(filepath: str, new_xml_content: str) -> str:
    """
    Updates a document
    Returns the updated document path if succesful
    """
    # Until we figure a rollback mechanism, this will never actually update the document,
    # in order to avoid data loss,
    # but instead generate an updated copy of the document
    filename, ext = path.splitext(filepath)
    copyfilepath = f"{filename}_copy{ext}"
    copy(filepath, copyfilepath)

    xmlzip.update_zip_inner_file(copyfilepath, new_xml_content)
    return copyfilepath


TOOLS = [copy_file, read_text_file, read_document_file_text_content,
         open_document_file_as_xml, update_document_with_xml]

# Explains the relationship between tools
TOOLS_PROMPT = f"""
- when opening a document, if no update is needed, open it as text directly rather than xml with {read_text_file.name}
- {update_document_with_xml.name} is supposed to be used in conjunction with {read_document_file_text_content.name}
"""
