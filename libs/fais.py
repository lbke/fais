import os
import sys
from typing import Optional, TypedDict

from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent

import argparse

from libs.contexteng.agents_md_resolver import resolve_agent_md
from libs.tools.thunderbird import TOOLS as thunderbird_tools
from libs.tools.documents import TOOLS as document_tools, TOOLS_PROMPT as document_tools_prompt
from libs.tools.planning import TOOLS as planning_tools
from libs.tools.fileexplorer import TOOLS as fileexplorer_tools
from libs.ui.print_langchain_chunk import print_chunk

from rich.console import Console
console = Console()

ALL_TOOLS = [*document_tools, *planning_tools,
             *fileexplorer_tools, *thunderbird_tools]

parser = argparse.ArgumentParser(
    prog='do',
    description='Lightweight CLI AI agent',
    epilog='MIT licence - LBKE')

parser.add_argument("prompt")
parser.add_argument("files", nargs="*")

BIG_MODEL = "mistral-large-latest"
SMALL_MODEL = "mistral-small-latest"
model = ChatMistralAI(
    model_name=SMALL_MODEL
)


agent = create_agent(
    model=model,
    system_prompt="""
    You are "fais", an AI agent running as a CLI.
    You speak French fluently.

    You must operate administrative tasks on files.
    Use the tools at your disposal to achieve the task assigned by the user.

    When tasked to read a file, never invent fake content.

    Do not propose any subsequent task, just do what you are asked.

    ## Tools at your disposal
    - Handling text documents: {document_tools_prompt}
    - Exploring files and folders
    - Planning events in a calendar, handling a schedule
""",
    tools=[
        *ALL_TOOLS
    ]
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


def build_context(work_dir):
    agent_md_path, agent_md_content = resolve_agent_md(work_dir)
    if agent_md_path is None:
        console.print("No AGENTS.md found, using empty context",
                      style="magenta")
        return ""
    console.print(
        f"AGENTS.md found at {agent_md_path}, using its content as context", style="magenta")
    return agent_md_content


def build_prompt(args: ParsedArgs):
    user_prompt = f"""
    Message de l'utilisateur:
    {args["prompt"]}
    """
    # meta_prompt = f"""
    # Tu es exécuté dans le dossier
    # """
    prompt = f"{user_prompt}"
    if (args["files"]):
        file_prompt = f"""
Fichiers fournis:
{args["files"]}
"""
        prompt = prompt+"\n"+file_prompt
    return prompt


def fais(argv):
    working_dir = os.getcwd()
    """
    [prompt, file1, file2...]
    """
    args = validate_args(argv)
    prompt = build_prompt(args)
    context = build_context(working_dir)
    final_prompt = f"""
    Prompt:
    {prompt}
    Context:
    {context}
    """

    # @see https://forum.langchain.com/t/prevent-last-llm-call-after-tool-calls/3063
    messages = []
    for chunk in agent.stream({"messages": final_prompt}):
        print_chunk(chunk)
    return messages


def main():
    console.print(
        f"[bright_black i]Running from {sys.argv[0]}[/bright_black i]")
    fais(sys.argv[1:])


if __name__ == "__main__":
    main()
