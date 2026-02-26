import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from pydantic import BaseModel, Field
import subprocess


# From https://github.com/patrup/mcp-libre/blob/main/src/libremcp.py

class TextContent(BaseModel):
    """Text content extracted from a document"""
    content: str = Field(description="The extracted text content")
    word_count: int = Field(description="Number of words in the content")
    char_count: int = Field(description="Number of characters in the content")
    page_count: Optional[int] = Field(
        description="Number of pages (if available)")


def _extract_xml_from_odt(file_path: str) -> str:
    import zipfile
    import xml.etree.ElementTree as ET
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Read content.xml from the ODT file
            content_xml = zf.read('content.xml').decode('utf-8')
            return content_xml
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from ODT: {str(e)}")


def _extract_text_from_odt(file_path: str) -> str:
    """Extract text content directly from ODT file"""
    import zipfile
    import xml.etree.ElementTree as ET

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Read content.xml from the ODT file
            content_xml = _extract_xml_from_odt(file_path)

            # Parse XML and extract text
            root = ET.fromstring(content_xml)

            # Find all text elements (simplified extraction)
            text_parts = []
            for elem in root.iter():
                if elem.text:
                    text_parts.append(elem.text)
                if elem.tail:
                    text_parts.append(elem.tail)

            return ' '.join(text_parts).strip()

    except Exception as e:
        raise RuntimeError(f"Failed to extract text from ODT: {str(e)}")


def _run_libreoffice_command(args: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
    """Run a LibreOffice command with proper error handling"""
    try:
        # Try different common LibreOffice executable names
        for executable in ['libreoffice', 'loffice', 'soffice']:
            try:
                cmd = [executable] + args
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    check=False
                )
                if result.returncode == 0 or executable == 'soffice':  # soffice might work even if return code != 0
                    return result
            except FileNotFoundError:
                continue

        raise FileNotFoundError(
            "LibreOffice executable not found. Please install LibreOffice.")
    except subprocess.TimeoutExpired:
        raise TimeoutError(
            f"LibreOffice command timed out after {timeout} seconds")


def read_document_text(path: str) -> TextContent:
    """Extract text content from a LibreOffice document

    Args:
        path: Path to the document file
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    try:
        # Use LibreOffice to convert to plain text
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = _run_libreoffice_command([
                '--headless',
                '--convert-to', 'txt',
                '--outdir', tmp_dir,
                str(path_obj)
            ])

            # Debug: check what files were created
            tmp_path = Path(tmp_dir)
            created_files = list(tmp_path.iterdir())

            # Look for the converted text file
            txt_file = None
            # Try different possible names
            possible_names = [
                path_obj.stem + '.txt',
                path_obj.name + '.txt',
                'output.txt'
            ]

            for name in possible_names:
                candidate = tmp_path / name
                if candidate.exists():
                    txt_file = candidate
                    break

            # If no specific file found, try any .txt file
            if not txt_file:
                txt_files = list(tmp_path.glob('*.txt'))
                if txt_files:
                    txt_file = txt_files[0]

            if txt_file and txt_file.exists():
                content = txt_file.read_text(encoding='utf-8', errors='ignore')
            else:
                # Fallback: try to extract text directly from ODT if it's a zip file
                if path_obj.suffix.lower() == '.odt':
                    content = _extract_text_from_odt(str(path_obj))
                else:
                    # Last resort: read as plain text
                    try:
                        content = path_obj.read_text(
                            encoding='utf-8', errors='ignore')
                    except:
                        raise RuntimeError(
                            f"Could not extract text. LibreOffice output: {result.stderr}. Files created: {[f.name for f in created_files]}")

        word_count = len(content.split())
        char_count = len(content)

        return TextContent(
            content=content,
            word_count=word_count,
            char_count=char_count,
            page_count=None  # Page count would require more complex parsing
        )

    except Exception as e:
        raise RuntimeError(f"Failed to read document: {str(e)}")


if __name__ == "__main__":
    res = _extract_xml_from_odt("./tests/hello.odt")
    print(res)
    # write extracted XML to a copy file in text mode
    with open("./tests/hello_copy.odt", 'w', encoding='utf-8') as copy:
        copy.write(res)
