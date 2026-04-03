from rich.console import Console
console = Console(style="dim")


def print_debug(*args):
    console.print(*args, style="dim")
