import subprocess
import typer
from typing import Optional, List
import os
import importlib.util
import sys

app = typer.Typer(help="Sungen Aider Plugin for AI-assisted coding tasks", name="aider")


def run_aider_command(args: List[str], stream: bool = True):
    """
    Run an Aider command with the provided arguments.

    Args:
        args (list): List of arguments for the Aider CLI command.
        stream (bool): Enable/disable streaming responses.
    """
    try:
        cmd = ['aider'] + args
        if not stream:
            cmd.append('--no-stream')
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running Aider command: {e.stderr}")


@app.command()
def message(model: str, prompt: str, files: Optional[List[str]] = typer.Argument(None)):
    """Send a message to Aider to perform a specific task on specified files."""
    args = ['--model', model, '--message', prompt]
    if files:
        args.extend(files)
    run_aider_command(args)


@app.command()
def generate(language: str, description: str, output_file: str):
    """Generate code or scripts in the specified language and save to a file."""
    prompt = f"Generate {language} code: {description}"
    run_aider_command(['--message', prompt, '--file', output_file])


@app.command()
def refactor(file: str, changes: str):
    """Refactor or modify the code in the given file."""
    prompt = f"Refactor the code in {file}: {changes}"
    run_aider_command(['--message', prompt, file])


@app.command()
def lint(file: Optional[str] = None, auto_fix: bool = False):
    """Perform linting checks on the specified file or all files."""
    args = ['--lint']
    if auto_fix:
        args.append('--auto-lint')
    if file:
        args.extend(['--file', file])
    run_aider_command(args)


@app.command()
def setup(model: str, api_key: str):
    """Setup Aider with the specified model and API key."""
    key_var = 'OPENAI_API_KEY' if 'gpt' in model else 'ANTHROPIC_API_KEY'
    os.environ[key_var] = api_key
    print(f"Aider setup complete with model {model}.")


@app.command()
def interactive(model: str = "gpt-4o-mini", files: Optional[List[str]] = typer.Argument(None)):
    """Enter interactive mode with Aider using the specified model and optional files."""
    args = ['--model', model]
    if files:
        args.extend(files)
    run_aider_command(args)


@app.command()
def commit(message: Optional[str] = None):
    """Commit all pending changes with an optional commit message."""
    args = ['--commit']
    if message:
        args.extend(['--commit-prompt', message])
    run_aider_command(args)


def check_installation():
    """
    Check if aider-chat is installed and install it if not present.
    Also check for API keys and warn if both are missing.
    """
    try:
        if importlib.util.find_spec("aider") is None:
            print("aider-chat is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "aider-chat"])
            print("aider-chat has been installed successfully.")

        openai_key = os.environ.get('OPENAI_API_KEY')
        anthropic_key = os.environ.get('ANTHROPIC_API_KEY')

        if not openai_key and not anthropic_key:
            print("Warning: Both OPENAI_API_KEY and ANTHROPIC_API_KEY are missing. At least one is recommended for Aider.")
    except Exception as e:
        print(f"Error during installation check: {str(e)}")


def register_plugin(parent_app: typer.Typer):
    """
    Register the plugin with the main application.
    """
    try:
        check_installation()
        parent_app.add_typer(app)
    except Exception as e:
        print(f"Failed to register plugin '{app}': {str(e)}")


if __name__ == "__main__":
    app()
