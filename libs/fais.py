import sys

from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent

import argparse

from libs.tools.documents import open_document, update_document

parser = argparse.ArgumentParser(
    prog='do',
    description='Lightweight CLI AI agent',
    epilog='MIT licence - LBKE')

parser.add_argument("prompt")
parser.add_argument("files", nargs="*")

model = ChatMistralAI(
    model_name="mistral-small-2506"
)


agent = create_agent(
    model=model,
    system_prompt="""
    Tu es "do", un agent IA exécuté dans un terminal.
    Tu dois exécuter des tâches bureatiques sur des fichiers.
    Mobilise les outils qui te sont fournis pour accomplir ces tâches.

    Si un prompt fait référence à un fichier
    mais qu'il n'apparaît pas dans la liste des fichiers,
    n'invente pas de contenu et préviens l'utilisateur.
""",
    tools=[update_document, open_document]
)


def run(argv):
    args = parser.parse_args(args=argv)
    print(args)
    if not args.prompt:
        print("Bonjour !")
        exit(0)
    user_prompt = f"""
    Message de l'utilisateur:
    {args.prompt}
    Fichiers fournis:
    {args.files}
    """
    # @see https://forum.langchain.com/t/prevent-last-llm-call-after-tool-calls/3063
    for chunk in agent.stream({"messages": user_prompt}):
        if "model" in chunk:
            for msg in chunk["model"]["messages"]:
                msg.pretty_print()


def main():
    run(sys.argv)


if __name__ == "__main__":
    main()
