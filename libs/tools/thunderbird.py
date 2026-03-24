import email
from os import path
import subprocess
from typing import Optional, TypedDict

from langchain.tools import tool


class EmailContent(TypedDict):
    subject: str
    to: str
    body: str
    """ Must be an absolute path"""
    attachment: Optional[str]


@tool(
    # Composing a mail should be a final action for now,
    # as it opens a new window in TB
    # TODO: Investigate a real CLI mail client like Himalaya for a more advanced email tool
    return_direct=True)
def compose_draft_email_thunderbird(emailContent: EmailContent):
    """
    Compose a draft email, using Thunderbird.

    """
    # https://kb.mozillazine.org/Command_line_arguments_-_Thunderbird
    attachment = emailContent.get("attachment", "")
    if attachment:
        if not path.exists(attachment):
            return f"Attachement file {attachment} doesn't exist"
        if not path.isabs(attachment):
            print("WARNING:",
                  f"Attachment file path must be absolute, got {attachment}")
            attachment = path.abspath(attachment)
    # For safety reasons, "to" is voluntarily made wrong
    # so we reduce the risk of an accidental send / piracy
    to = emailContent.get("to", "")
    safe_to = f"~~{to}~~" if to else ""
    mail_content = "subject='{subject}',to='{to}',body='{body}',attachment='{attachment}'".format(
        subject=emailContent.get("subject", ""),
        to=safe_to,
        body=emailContent.get("body", ""),
        attachment=attachment
    )
    print(mail_content)
    res = subprocess.run(
        ["thunderbird", "-compose", mail_content])
    print(mail_content)
    return res.returncode


TOOLS = [compose_draft_email_thunderbird]
