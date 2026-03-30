from langchain.messages import AIMessage, ToolMessage
from langchain_core.messages.tool import tool_call

PREFIX = "| • "


def print_chunk(chunk):
    print(chunk)
    if "model" in chunk:
        print_ai_chunk(chunk)
    elif "tools" in chunk:
        print_tool_chunk(chunk)
    else:
        print("=== Chunk ===")
        print(chunk)


def print_ai_chunk(chunk):
    msg: AIMessage = chunk["model"]["messages"][-1]
    if len(msg.tool_calls):
        if len(msg.tool_calls) > 1:
            print(PREFIX, f"Multiple tool calls: {len(msg.tool_calls)}")
        for tc in msg.tool_calls:
            print(PREFIX, f"Tool call: {tc["name"]} (id: {tc["id"]})")
            print(PREFIX, f"| Args: {tc["args"]}")
    else:
        print(PREFIX, f"Fais dis:")
        print(f"{msg.content}")


def print_tool_chunk(chunk):
    """
    An AI Message can trigger multiple tool calls, but the stream will return one tool message at a time.

    """
    msg: ToolMessage = chunk["tools"]["messages"][-1]
    print(f"Tool result: {msg.name} (id: {msg.tool_call_id})")
    print(f"| Result: {msg.content}")
