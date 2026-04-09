from dataclasses import dataclass
import email
from os import path
import re
import subprocess
from typing import Optional

from langchain.tools import tool


# dataclass is the best way to get schema + custom methods
# (Pydantic would require clumsy JSON syntax ; TypedDict doesn't support methods)
@dataclass
class EmailContent:
    subject: str
    to: str
    body: str
    """ Must be an absolute path"""
    attachment: Optional[str] = None  # default value matters even when using Optional with dataclass

    def generate_email(self):
        to = getattr(self, "to", "")
        safe_to = f"~~{to}~~" if to else ""
        mail_content = "subject='{subject}',to='{to}',body='{body}'".format(
            subject=getattr(self, "subject", ""),
            to=safe_to,
            body=getattr(self, "body", ""),
        )
        attachment = getattr(self, "attachment", "")
        if attachment:
            if not path.exists(attachment):
                return f"Attachment file {attachment} doesn't exist"
            if not path.isabs(attachment):
                print("WARNING:",
                      f"Attachment file path must be absolute, got {attachment}")
                attachment = path.abspath(attachment)
            mail_content += f",attachment='{attachment}'"
        return mail_content


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
    # For safety reasons, "to" is voluntarily made wrong
    # so we reduce the risk of an accidental send / piracy
    mail_content = emailContent.generate_email()
    res = subprocess.run(
        ["thunderbird", "-compose", mail_content])
    return res.returncode


TOOLS = [compose_draft_email_thunderbird]
