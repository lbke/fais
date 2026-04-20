from typing import TypedDict

from langchain_core.messages.tool import tool_call
from langchain.messages import AIMessage, HumanMessage, ToolMessage
from rich.console import Console
debug_console = Console(style="dim")
info_console = Console(style="dim magenta")
console = Console(style="grey74")
final_console = Console(style="bright_white")
PREFIX = "[cyan]•[/cyan][blue]•[/blue][green]•[/green] "

# LangGraph typings are terrible and somehow langchain agents don't improve them...


class TerminalEventPrinter():
    def print_debug(self, *args):
        debug_console.print(*args, style="dim")

    def print_info(self, *args):
        info_console.print(*args)

    # LangChain elements
    def print_model_data(self, data):
        msg: AIMessage = data["model"]["messages"][-1]
        if len(msg.tool_calls):
            if len(msg.tool_calls) > 1:
                console.print(
                    PREFIX, f"Multiple tool calls: {len(msg.tool_calls)}")
            for tc in msg.tool_calls:
                console.print(
                    PREFIX, f"Tool call: {tc["name"]} (id: {tc["id"]})")
                console.print(PREFIX, f"Args: {tc["args"]}")
        else:
            console.print(PREFIX, f"Fais dis:", style="bold")
            final_console.print(f"{msg.content}", style="bright_white")

    def print_tool_data(self, data):
        """
        An AI Message can trigger multiple tool calls, but the stream will return one tool message at a time.

        """
        msg: ToolMessage = data["tools"]["messages"][-1]
        console.print(
            PREFIX, f"Tool result for: {msg.name} (id: {msg.tool_call_id})")
        content = msg.content
        if (len(content) > 100):
            content = content[0:97] + "..."
        console.print(PREFIX, f"Result: {content}")

    def print_chunk(self, chunk):
        if chunk["type"] != "updates":
            print("Unknown chunk type:", chunk["type"])
            return
        # print(chunk)
        data = chunk["data"]
        if "model" in data:
            self.print_model_data(data)
        elif "tools" in data:
            self.print_tool_data(data)
        elif "HumanInTheLoopMiddleware.after_model" in data:
            pass
        else:
            console.print(PREFIX, "Chunk")
            console.print(chunk)

    # def input_hil():


# Default singleton for display
tp = TerminalEventPrinter()
