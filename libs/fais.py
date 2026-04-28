import os
import sys
import uuid

from httpx import HTTPStatusError
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from langgraph.types import Command, StreamPart
from prompt_toolkit.shortcuts import choice
from prompt_toolkit.filters import is_done


from libs.cli.parse_args import parse_args
from libs.contexteng.prompt_builder import build_context, build_prompt
from libs.tools.thunderbird import TOOLS as thunderbird_tools
from libs.tools.documents import TOOLS as document_tools, TOOLS_PROMPT as document_tools_prompt, copy_file
from libs.tools.planning import TOOLS as planning_tools
from libs.tools.fileexplorer import TOOLS as fileexplorer_tools
from libs.tools.internet import TOOLS as internet_tools
from libs.display.terminal_printer import tp
from langgraph.checkpoint.memory import InMemorySaver


from rich.console import Console
console = Console()


ALL_TOOLS = [*document_tools, *planning_tools,
             *fileexplorer_tools, *thunderbird_tools, *internet_tools]


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
    config = {"configurable": {"thread_id": uuid.uuid4().hex}}
    # initial command = user prompt
    # may be replace by "resume" commands after interrupts
    command = {"messages": final_prompt}
    while RUN_LOOP:
        # Immediately break loop unless an interrupt is triggered
        RUN_LOOP = False
        # TODO: when rejecting a tool call, the agent may stream an interrupt again
        # => remember rejected tool calls and prevent the interruption in this case
        try:
            # FIXME : type inference is wrong, and using "StreamPart" from "langgraph.types" doesn't work
            # since it lacks the proper generic type for data (using AgentState)
            # so not typing for chunks for now...
            for chunk in agent.stream(command, config=config, version='v2'):
                if is_debug():
                    tp.print_debug(f"Chunk received: {chunk}")
                tp.print_chunk(chunk)
                if chunk["type"] == "updates" and chunk["data"].get("__interrupt__"):
                    RUN_LOOP = True
                    # Interrupt values are still untyped
                    interrupt_val = chunk["data"]["__interrupt__"][0].value
                    if is_debug():
                        tp.print_debug(interrupt_val)
                    decisions = []
                    for action in interrupt_val["action_requests"]:
                        # NOTE: zipping could work but not sure if order is guaranteed
                        review_config = next(rc for rc in
                                             interrupt_val["review_configs"] if rc["action_name"] == action["name"])
                        # https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_a_choice.html
                        # (value, message)
                        options = [(o, o)
                                   for o in review_config["allowed_decisions"]]
                        response = choice(
                            message=f"Interrupt received for action {action['name']}({action['args']}).", show_frame=~is_done, options=options)
                        decision = {"type": response}
                        # TODO: not finalized, need to
                        if response == "edit":
                            decision["edited_action"] = console.input(
                                "Proposed edit?")
                        decisions.append(decision)
                    command = Command(resume={"decisions": decisions})
                # Prevent running too many steps
                count_stream_steps += 1
                if count_stream_steps > MAX_STREAM_STEPS:
                    tp.print_debug(
                        f"Maximum number of stream steps ({MAX_STREAM_STEPS}) reached, stopping the stream to prevent infinite loop.")
                    break
        except HTTPStatusError as e:
            if e.response.status_code == 401:
                tp.print_debug(
                    "Unauthorized error during agent execution. This may be due to an invalid API key.")
            tp.print_debug(f"HTTP error during agent execution: {e}")
    return agent.get_state(config).values["messages"]


def main():
    console.print(
        f"[bright_black i]Running from {sys.argv[0]}[/bright_black i]")
    fais(sys.argv[1:])


if __name__ == "__main__":
    main()
