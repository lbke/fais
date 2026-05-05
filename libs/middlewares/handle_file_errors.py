from functools import wraps
from zipfile import BadZipFile

from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools import ToolException


@wrap_tool_call
def HandleFileErrorsMiddleware(request, handler):
    """

    Catch common exceptions related to opening common types of files
    Transforms them in strings so the agent can react to them
    For more exotic exception, use specialized middlewares
    """
    try:
        return handler(request)
    except (FileNotFoundError, NotADirectoryError, BadZipFile) as err:
        # Accourding to documentation, tool exception doesn't stop an agent from running
        # FIXME: this doesn't work as expected, the ToolException is not caught by the agent
        # See this feature request: https://github.com/langchain-ai/langchain/issues/37195
        # raise ToolException(err)
        return ToolMessage(content=str(err), tool_call_id=request.tool_call["id"])
