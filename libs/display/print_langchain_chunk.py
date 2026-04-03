from langchain.messages import AIMessage, ToolMessage
from langchain_core.messages.tool import tool_call
from rich.console import Console
console = Console(style="grey74")
final_console = Console(style="bright_white")
PREFIX = "[cyan]•[/cyan][blue]•[/blue][green]•[/green] "


def print_chunk(chunk):
    # print(chunk)
    if "model" in chunk:
        print_ai_chunk(chunk)
    elif "tools" in chunk:
        print_tool_chunk(chunk)
    else:
        console.print(PREFIX, "Chunk")
        console.print(chunk)


def print_ai_chunk(chunk):
    msg: AIMessage = chunk["model"]["messages"][-1]
    if len(msg.tool_calls):
        if len(msg.tool_calls) > 1:
            console.print(
                PREFIX, f"Multiple tool calls: {len(msg.tool_calls)}")
        for tc in msg.tool_calls:
            console.print(PREFIX, f"Tool call: {tc["name"]} (id: {tc["id"]})")
            console.print(PREFIX, f"Args: {tc["args"]}")
    else:
        console.print(PREFIX, f"Fais dis:", style="bold")
        final_console.print(f"{msg.content}", style="bright_white")


def print_tool_chunk(chunk):
    """
    An AI Message can trigger multiple tool calls, but the stream will return one tool message at a time.

    """
    msg: ToolMessage = chunk["tools"]["messages"][-1]
    console.print(
        PREFIX, f"Tool result for: {msg.name} (id: {msg.tool_call_id})")
    content = msg.content
    if (len(content) > 100):
        content = content[0:97] + "..."
    console.print(PREFIX, f"Result: {content}")
