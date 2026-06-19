from os import path
from shutil import copy

from langchain.tools import tool

from libs.utils import xmlzip
from xml.etree import ElementTree

from libs.utils.xmleditor import edit_xml_node_text, xml_file_to_selectable_text_map


@tool
def open_document_file_as_xml(filepath: str) -> str:
    """
    Use to open .docx or .odt documents
    (Microsoft Word, Libre Office files).

    Do not use for other types of files such as PDF,
    since they are not zipped XML files.

    Returns the file's main content structured in XML
    The XML can be edited to create a new file, as long as the structure is respected.
    """
    return xmlzip.extract_content_xml_from_zip(filepath)


@tool
def open_xml_file_for_edit(filepath: str) -> str:
    """
    Returns a map of XML selectors and text content for a document file (docx, odt)
    This is ideal for document edition with no risk of breaking the XML structure
    Use this tool to open XML documents if you plan to edit them.
    """
    xml_content = xmlzip.extract_content_xml_from_zip(filepath)
    xml_map = xml_file_to_selectable_text_map(xml_content)
    return xml_map


@tool
def edit_xml_file_content(selector: str, new_text: str, filepath: str) -> str:
    """
    Edit an XML document (docx, odt) by specifying a selector and new text content
    It has no risk of accidentally breaking the XML structure, since it only edits the text content of a node.
    Use {open_xml_file_for_edit} to get the selectors and text content map for a document.
    """
    xml_content = xmlzip.extract_content_xml_from_zip(filepath)
    try:
        updated_xml = edit_xml_node_text(selector, new_text, xml_content)
    except ValueError as e:
        return f"Error editing node {selector} in {filepath}: {str(e)}"
    xmlzip.update_zip_inner_file(filepath, updated_xml)
    return f"Succesfully edited node {selector} in {filepath}."


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
    text_chunks = [chunk.strip() for chunk in root.itertext()
                   if chunk and chunk.strip()]

    return " ".join(text_chunks)


@tool
def update_document_with_xml(filepath: str, new_xml_content: str) -> str:
    """
    Updates a document
    Returns the updated document path if succesful
    """
    # Until we figure a rollback mechanism and better XML edits,
    # this will not actually update the document,
    # in order to avoid data loss,
    # but instead generate an updated copy of the document
    filename, ext = path.splitext(filepath)
    copyfilepath = f"{filename}_copy{ext}"
    copy(filepath, copyfilepath)

    xmlzip.update_zip_inner_file(copyfilepath, new_xml_content)
    return copyfilepath


TOOLS = [edit_xml_file_content, open_xml_file_for_edit, read_text_file, read_document_file_text_content,
         open_document_file_as_xml, update_document_with_xml]

# Explains the relationship between tools
TOOLS_PROMPT = f"""
- when opening a document, if no update is needed, open it as text directly rather than xml with {read_text_file.name}
- {update_document_with_xml.name} is supposed to be used in conjunction with {read_document_file_text_content.name}
"""
