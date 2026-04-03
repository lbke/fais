from build.lib.libs.fais import ParsedArgs
from libs.contexteng.agents_md_resolver import resolve_agent_md
from libs.display.print_info import print_info


def build_context(work_dir):
    agent_md_path, agent_md_content = resolve_agent_md(work_dir)
    if agent_md_path is None:
        print_info("No AGENTS.md found, using empty context")
        return ""
    print_info(
        f"AGENTS.md found at {agent_md_path}, using its content as context")
    return agent_md_content


def build_prompt(args: ParsedArgs):
    user_prompt = f"""
    Message de l'utilisateur:
    {args["prompt"]}
    """
    # meta_prompt = f"""
    # Tu es exécuté dans le dossier
    # """
    prompt = f"{user_prompt}"
    if (args["files"]):
        file_prompt = f"""
Fichiers fournis:
{args["files"]}
"""
        prompt = prompt+"\n"+file_prompt
    return prompt
