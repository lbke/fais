"""
Allow agent to trigger a direct return for their last tool call
The return_direct tool acts as a "tag" that is detected

Possible alternative implementation:
- a wrap_model_call middleware could work to replace the after_model and before_model,
but the agent jump system is probably more explicit
- the return_direct option of the tool cannot be controlled easily by the model
- wrapping all tools so there is an additional hidden "return_direct" argument controlled by the LLM: might be simpler but behaviour is not clear if there are parallel tool calls (what if only one has the return_direct tag?)
"""


import pprint

from langchain.agents import AgentState
from langchain.agents.middleware import Runtime, after_model, before_model, hook_config, wrap_model_call
from langchain.messages import AIMessage, ToolMessage
from langchain.tools import tool
from libs.display.terminal_printer import tp


@tool
def return_direct():
    """
    Use this tool in parallel to other tools whenever you think the tools direct output will be enough to answer the user questions
    This reduces costs by avoiding a useless LLM inference
    - If multiple tools must be called in a sequence call only for the LAST tool in the sequence
    - Use this tool in parallel with the tools that you want to return directly, not AFTER (otherwise it is useless)
    - Never call this tool alone, it should always be called with other tools
    """
    return


@after_model
def detect_return_direct(state: AgentState, runtime: Runtime):
    """
    Detect LLM calls to the return_direct tool and set a flag in the context
    Alternative : parse messages everytime in apply_return_direct,
    but it would be more compute intensive
    """
    last_msg = state["messages"][-1]
    pprint.pprint(last_msg)

    # Detect a call to "return_direct" tool
    if isinstance(last_msg, AIMessage):
        return_direct = next(
            (tc for tc in last_msg.tool_calls if tc["name"] == "return_direct"), None)
        print("Has return_direct been called?", bool(return_direct))
        if return_direct:
            # unknow state field are dismissed so use context instead to flag return_direct calls
            runtime.context["return_direct_called"] = True
            runtime.context["return_direct_expected_tool_calls"] = len(
                last_msg.tool_calls)
    return None


@before_model
@hook_config(can_jump_to=["end"])
def apply_return_direct(state: AgentState, runtime: Runtime):
    # If return_direct was called
    print("context", runtime.context.get("return_direct_called"))
    if runtime.context.get("return_direct_called", False):
        expected_tool_calls = runtime.context.get(
            "return_direct_expected_tool_calls")
        # Get latest tool calls
        idx = 1
        tool_msgs = []
        while idx <= len(state["messages"]):
            msg = state["messages"][-idx]
            if isinstance(msg, ToolMessage):
                tool_msgs.append(msg)
                idx += 1
            else:
                break
        # We are still waiting for some tool messages
        # TODO: doesn't that really ever happens in a wrap_model middleware? Since tool calls are handled separately, we may always have all the tools here?
        if len(tool_msgs) < expected_tool_calls:
            tp.print_info(
                f"Waiting for more tool calls (got {len(tool_msgs)} over{expected_tool_calls}), returning intermediate content")
            return None
        # We have collected all tool calls, we can return the aggregated content
        agg_content = ""
        for msg in tool_msgs:
            agg_content += f"Output of tool {msg.name}:\n{msg.content}"
        state["messages"].append(AIMessage(content=agg_content))
        # Alternative implementation would be using wrap_model_call and return "request" with no handler call
        # https://docs.langchain.com/oss/python/langchain/middleware/custom#agent-jumps
        return {"messages": AIMessage(content=agg_content), "jump_to": "end"}
    return None


ReturnDirectMiddlewares = [apply_return_direct, detect_return_direct]
