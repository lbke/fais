import os
import sys

from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent

from build.lib.libs.fais import build_prompt
from libs.cli import parse_args
from libs.contexteng.prompt_builder import build_context
from libs.tools.thunderbird import TOOLS as thunderbird_tools
from libs.tools.documents import TOOLS as document_tools, TOOLS_PROMPT as document_tools_prompt, copy_file
from libs.tools.planning import TOOLS as planning_tools
from libs.tools.fileexplorer import TOOLS as fileexplorer_tools
from libs.display.print_debug import print_debug
from libs.display.print_langchain_chunk import print_chunk

from rich.console import Console
console = Console()

ALL_TOOLS = [*document_tools, *planning_tools,
             *fileexplorer_tools, *thunderbird_tools]


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
    ],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                [copy_file.__name__]: True
            },
        )
    ]
)


def is_debug():
    return os.getenv("DEBUG")


def fais(argv):
    working_dir = os.getcwd()
    """
    [prompt, file1, file2...]
    """
    args = parse_args(argv)
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
        if is_debug():
            print_debug(f"Chunk received: {chunk}")
        print_chunk(chunk)
    return messages


def main():
    console.print(
        f"[bright_black i]Running from {sys.argv[0]}[/bright_black i]")
    fais(sys.argv[1:])


if __name__ == "__main__":
    main()
