"""llm"""
import json
from pathlib import Path

import typer

from sungen.utils.chat_tools import chatbot
from sungen.utils.dspy_tools import GPT_DEFAULT_MODEL

app = typer.Typer()


@app.command(name="chat")
def _chat():
    """chat"""
    typer.echo("Running chat subcommand.")


@app.command(name="ask")
def ask_question(
        question: str = typer.Argument(..., help="Single question for the chatbot about plugin_cmd.py"),
        model: str = typer.Option(GPT_DEFAULT_MODEL,
                                  help="Model to use for the chatbot (e.g., gpt-4-turbo, qwen2:instruct)")
):
    """
    CLI Command: Ask a single question about the plugin_cmd.py file using the specified model.
    """
    # Get the content of plugin_cmd.py
    plugin_cmd_path = Path(__file__)
    plugin_cmd_content = plugin_cmd_path.read_text()

    # Get CLI help information for this file
    cli_help = get_cli_help(plugin_cmd_content)

    # Prepare the context for the chatbot
    context = f"""
    File: plugin_cmd.py

    CLI Commands:
    {cli_help}

    File Content:
    {plugin_cmd_content}
    """

    # Ask the question and get the response
    typer.echo(f"Asking question using model: {model}...")
    response = chatbot(question=question, context=context, model=model)

    typer.echo(f"Answer: {response}")


def crawl_cli_help(app: typer.Typer, output_file: str = "cli_help.json"):
    """
    Crawl the Typer CLI help and save it to a JSON file.
    """
    help_data = {}

    def crawl_commands(typer_app, prefix=""):
        for command in typer_app.registered_commands:
            full_name = f"{prefix}{command.name}"
            help_data[full_name] = {
                "help": command.help,
                "arguments": [],
                "options": []
            }
            for param in command.params:
                if param.param_type_name == "argument":
                    help_data[full_name]["arguments"].append({
                        "name": param.name,
                        "help": param.help
                    })
                elif param.param_type_name == "option":
                    help_data[full_name]["options"].append({
                        "name": param.name,
                        "help": param.help
                    })

        for group in typer_app.registered_groups:
            group_prefix = f"{prefix}{group.name} "
            crawl_commands(group.typer_instance, group_prefix)

    crawl_commands(app)

    with open(output_file, "w") as f:
        json.dump(help_data, f, indent=2)

    typer.echo(f"CLI help saved to {output_file}")


@app.command(name="save-help")
def save_cli_help(
        output_file: str = typer.Option("cli_help.json", help="Output file for the CLI help")
):
    """
    CLI Command: Crawl the Typer CLI help and save it to a JSON file.
    """
    crawl_cli_help(app, output_file)


def get_cli_help(plugin_source: str) -> str:
    """Extract CLI help information from the plugin source code."""
    import types
    import sys
    from io import StringIO

    # Create a temporary module to execute the plugin code
    temp_module = types.ModuleType('temp_plugin')
    exec(plugin_source, temp_module.__dict__)

    # Check if the module has a Typer app
    if hasattr(temp_module, 'app') and isinstance(temp_module.app, typer.Typer):
        # Capture the help output
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            temp_module.app(["--help"], standalone_mode=False)
        except SystemExit:
            pass
        finally:
            help_output = sys.stdout.getvalue()
            sys.stdout = old_stdout
        return help_output
    else:
        return "No CLI commands found in this plugin."