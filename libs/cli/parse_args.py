import os
import argparse
from typing import Optional, TypedDict


class ParsedArgs(TypedDict):
    prompt: str
    files: Optional[list[str]]


parser = argparse.ArgumentParser(
    prog='do',
    description='Lightweight CLI AI agent',
    epilog='MIT licence - LBKE')

parser.add_argument("prompt")
parser.add_argument("files", nargs="*")


def parse_args(argv):
    args = parser.parse_args(args=argv)
    if not args.prompt:
        print("Bonjour !")
        exit(0)
    if len(args.prompt) > 10000:
        print("Prompt too big")
        exit(1)
    for f in (args.files or []):
        if not os.path.exists(f):
            raise ValueError(f"File doesn't exist: {f}")
    return {
        "prompt": args.prompt,
        "files": args.files or None
    }
