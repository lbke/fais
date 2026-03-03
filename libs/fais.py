import os
import sys
from typing import Optional, TypedDict

from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent

import argparse

from libs.tools.documents import open_document, update_document
from libs.tools.planning import planning_intersection

parser = argparse.ArgumentParser(
    prog='do',
    description='Lightweight CLI AI agent',
    epilog='MIT licence - LBKE')

parser.add_argument("prompt")
parser.add_argument("files", nargs="*")

model = ChatMistralAI(
    model_name="mistral-small-2506"
)


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
    tools=[update_document, open_document, planning_intersection]
)


class ParsedArgs(TypedDict):
    prompt: str
    files: Optional[list[str]]


def validate_args(argv):
    args = parser.parse_args(args=argv)
    if not args.prompt:
        print("Bonjour !")
        exit(0)
    if len(args.prompt) > 10000:
        print("Prompt too big")
        exit(1)
    for f in (args.files or []):
        if not os.path.exists(f):
            raise ValueError(f"File doesn't exist: {f}")
    return {
        "prompt": args.prompt,
        "files": args.files or None
    }


def build_prompt(args: ParsedArgs):
    user_prompt = f"""
    Message de l'utilisateur:
    {args["prompt"]}
    """
    prompt = f"{user_prompt}"
    if (args["files"]):
        file_prompt = f"""
Fichiers fournis:
{args["files"]}
"""
        prompt = prompt+"\n"+file_prompt
    return prompt


def run(argv):
    args = validate_args(argv)
    prompt = build_prompt(args)

    # @see https://forum.langchain.com/t/prevent-last-llm-call-after-tool-calls/3063
    last_msg = None
    for chunk in agent.stream({"messages": prompt}):
        if "model" in chunk:
            for msg in chunk["model"]["messages"]:
                msg.pretty_print()
                last_msg = msg
        else:
            print(chunk)
    return last_msg


def main():
    print(f"Running from {sys.argv[0]}")
    run(sys.argv[1:])


if __name__ == "__main__":
    main()
