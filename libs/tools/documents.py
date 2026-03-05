from os import path
from shutil import copy

from langchain.tools import tool

from libs.utils import xmlzip
from xml.etree import ElementTree


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
    return ElementTree(xml).tostring()


@tool
def update_document_with_xml(filepath: str, new_xml_content: str) -> str:
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
    xmlzip.update_zip_inner_file(copyfilepath, new_xml_content)
    return copyfilepath


TOOLS = [read_text_file, read_document_file_text_content,
         open_document_file_as_xml, update_document_with_xml]

# Explains the relationship between tools
TOOLS_PROMPT = f"""
- when opening a document, if no update is needed, open it as text directly rather than xml with {read_text_file.name}
- {update_document_with_xml.name} is supposed to be used in conjunction with {read_document_file_text_content.name}
"""
