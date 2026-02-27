from os import path
from shutil import copy
import sys

from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from libs import xmlzip

import argparse

parser = argparse.ArgumentParser(
    prog='do',
    description='Lightweight CLI AI agent',
    epilog='MIT licence - LBKE')

parser.add_argument("prompt")
parser.add_argument("files", nargs="*")

model = ChatMistralAI(
    model_name="mistral-small-2506"
)


@tool
def open_document(filepath: str) -> str:
    """
    Use to open .docx or .odt documents
    Returns their text content
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


agent = create_agent(
    model=model,
    system_prompt="""
    Tu es "do", un agent IA exécuté dans un terminal.
    Tu dois exécuter des tâches bureatiques sur des fichiers.
    Mobilise les outils qui te sont fournis pour accomplir ces tâches.

    Si un prompt fait référence à un fichier
    mais qu'il n'apparaît pas dans la liste des fichiers,
    n'invente pas de contenu et préviens l'utilisateur.
""",
    tools=[update_document, open_document]
)


def run(argv):
    args = parser.parse_args(args=argv)
    print(args)
    if not args.prompt:
        print("Bonjour !")
        exit(0)
    user_prompt = f"""
    Message de l'utilisateur:
    {args.prompt}
    Fichiers fournis:
    {args.files}
    """
    for chunk in agent.stream({"messages": user_prompt}):
        if "model" in chunk:
            for msg in chunk["model"]["messages"]:
                msg.pretty_print()


def main():
    run(sys.argv)

if __name__ == "__main__":
    main()
