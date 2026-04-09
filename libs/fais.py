import os
import sys
from urllib import response
import uuid

from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from langgraph.types import Command
from rich.prompt import Prompt


from libs.cli.parse_args import parse_args
from libs.contexteng.prompt_builder import build_context, build_prompt
from libs.tools.thunderbird import TOOLS as thunderbird_tools
from libs.tools.documents import TOOLS as document_tools, TOOLS_PROMPT as document_tools_prompt, copy_file
from libs.tools.planning import TOOLS as planning_tools
from libs.tools.fileexplorer import TOOLS as fileexplorer_tools
from libs.display.print_debug import print_debug
from libs.display.print_langchain_chunk import print_chunk
from langgraph.checkpoint.memory import InMemorySaver


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
                copy_file.name: True
            },
        )
    ],
    checkpointer=InMemorySaver(),
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

    MAX_STREAM_STEPS = 500
    count_stream_steps = 0
    RUN_LOOP = True
    messages = []
    config = {"configurable": {"thread_id": uuid.uuid4().hex}}
    # initial command = user prompt
    # may be replace by "resume" commands after interrupts
    command = {"messages": final_prompt}
    while RUN_LOOP:
        # Immediately break loop unless an interrupt is triggered
        RUN_LOOP = False
        # TODO: when rejecting a tool call, the agent may stream an interrupt again
        # => remember rejected tool calls and prevent the interruption in this case
        # TODO: switch to v2 https://forum.langchain.com/t/typing-of-streamed-chunks/3356
        for chunk in agent.stream(command, config=config):
            if is_debug():
                print_debug(f"Chunk received: {chunk}")
            # Handle interrupts
            if "__interrupt__" in chunk:
                RUN_LOOP = True
                interrupt_val = chunk["__interrupt__"][0].value
                print_debug(interrupt_val)
                decisions = []
                for action in interrupt_val["action_requests"]:
                    # NOTE: zipping could work but not sure if order is guaranteed
                    review_config = next(rc for rc in
                                         interrupt_val["review_configs"] if rc["action_name"] == action["name"])
                    # TODO: Prompt.ask is just a wrapper around the basic input,
                    # find a way a to get a proper list input for better UX
                    response = Prompt.ask(
                        f"Interrupt received for action {action['name']}({action['args']}).", choices=review_config["allowed_decisions"])
                    decision = {"type": response}
                    # TODO: not finalized
                    if response == "edit":
                        decision["edited_action"] = console.input(
                            "Proposed edit?")
                    decisions.append(decision)
                command = Command(resume={"decisions": decisions})

            # Prevent running too many steps
            count_stream_steps += 1
            if count_stream_steps > MAX_STREAM_STEPS:
                print_debug(
                    f"Maximum number of stream steps ({MAX_STREAM_STEPS}) reached, stopping the stream to prevent infinite loop.")
                break
    return messages


def main():
    console.print(
        f"[bright_black i]Running from {sys.argv[0]}[/bright_black i]")
    fais(sys.argv[1:])


if __name__ == "__main__":
    main()
