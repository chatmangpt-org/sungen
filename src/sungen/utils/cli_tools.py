import os
from importlib import import_module
from pathlib import Path
from github import Github

import dspy
import typer


class ChatbotAssistance(dspy.Signature):
    """
    Provides guidance and assistance to users in developing projects with sungen,
    leveraging the integrated chatbot functionality.
    """
    # The question or query from the user.
    question = dspy.InputField(desc="The user's query or request for assistance.")

    # The context or background information necessary for the chatbot to provide relevant assistance.
    context = dspy.InputField(desc="Background information relevant to the user's query.")

    # The history of the conversation, to maintain context and continuity.
    conversation_history = dspy.InputField(desc="Previous exchanges between the user and the chatbot, if any.")

    # The answer or guidance provided by the chatbot.
    answer = dspy.OutputField(desc="The chatbot's response to the user's query.")


def chatbot(question, context, history=""):
    if not question:
        question = typer.prompt("How can I help you?")

    qa = dspy.ChainOfThought(ChatbotAssistance)
    response = qa(question=question, context=context, conversation_history=history).answer
    history += response
    print(f"Chatbot: {response}")
    confirmed = False
    while not confirmed:
        confirm = typer.prompt("Did this answer your question? [y/N]", default="N")

        if confirm.lower() in ["y", "yes"]:
            confirmed = True
        else:
            want = typer.prompt("How can I help more?")

            response = qa(question=want, context=context, conversation_history=history).answer
            history += response
            print(f"Chatbot: {response}")

    return history


def load_commands(app, cmd_dir):
    # Convert cmd_dir to Path if it's a string
    cmd_dir = Path(cmd_dir) if isinstance(cmd_dir, str) else cmd_dir

    # Get the base module path relative to the package
    try:
        # Find the relative module path from the current package
        package_path = cmd_dir.resolve()
        module_base = ".".join(package_path.parts[-2:])  # Assumes cmds/ is a subdirectory of the package
    except IndexError:
        raise ValueError(f"The path '{cmd_dir}' does not appear to be within an importable package structure.")

    # Iterate over Python files in the command directory
    for filepath in cmd_dir.glob("*_cmd.py"):
        # Construct the full module name for import
        module_name = f"{module_base}.{filepath.stem}"
        try:
            module = import_module(module_name)
            if hasattr(module, "app"):
                # Add the module's app to the main app
                app.add_typer(module.app, name=filepath.stem[:-4], help=module.__doc__)
        except Exception as e:
            raise ValueError(f"Failed to load module '{module_name}'")


# Dependency injection for creating a GitHub instance
def get_github_instance(token: str = typer.Option(None, envvar="GITHUB_TOKEN")) -> Github:
    if not token:
        typer.echo("Error: No GitHub token provided and $GITHUB_TOKEN is not set.", err=True)
        raise typer.Exit(code=1)

    return Github(token)
