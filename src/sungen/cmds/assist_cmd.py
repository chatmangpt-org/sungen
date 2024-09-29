"""assist"""
import typer
import os
import tempfile
import subprocess
from sungen.plugins.blueprint.models.blueprint_models import CodeBlueprint  # Import the model
from pathlib import Path

app = typer.Typer()


@app.command(name="blueprint")
def _blueprint(echo: str):
    """blueprint"""
    typer.echo(f"Running blueprint subcommand: {echo}")


@app.command(name="run")
def run(file_path: Path = Path("./blueprint.yaml")):
    """run"""
    _run(file_path)


def _run(file_path: Path):
    """Run a specified blueprint from the given file path."""
    bp = CodeBlueprint.from_yaml(file_path)
    print(bp)

    for file in bp.files_to_create:
        directory = os.path.dirname(file)
        if directory and not os.path.exists(directory):
            typer.echo(f"Creating directory: {directory}")
            os.makedirs(directory)  # Create the missing directories
        if not os.path.exists(file):
            typer.echo(f"Creating file: {file}")
            with open(file, 'w') as f:
                f.write('')  # Create an empty file

    # Add logic to execute the blueprint here
    # For example, you might want to load the blueprint from the file path
    # blueprint = load_blueprint(file_path)
    # process_blueprint(blueprint)

def run_blueprint_logic(blueprint_file: str):
    """Logic for running a specified blueprint."""
    # Load the blueprint from the YAML file
    blueprint = CodeBlueprint.from_yaml(blueprint_file)

    # Step 1: Handle `files_to_create` - Create any files that are listed
    for file_to_create in blueprint.files_to_create:
        directory = os.path.dirname(file_to_create)
        if directory and not os.path.exists(directory):
            typer.echo(f"Creating directory: {directory}")
            os.makedirs(directory)  # Create the missing directories
        if not os.path.exists(file_to_create):
            typer.echo(f"Creating file: {file_to_create}")
            with open(file_to_create, 'w') as f:
                f.write('')  # Create an empty file for other types

    # Step 2: Construct the base aider command
    command = [
        "aider",
        "--model", blueprint.model,  # Use the specified AI model
        "--yes",  # Assume yes to all prompts for smoother automation
        # "--verbose",
        # "--no-stream"
    ]

    for file in (blueprint.files_to_edit + blueprint.files_to_create):
        command.extend(["--file", file])  # Specify files to change

    for read_only_file in blueprint.read_only_files:
        command.extend(["--read", read_only_file])  # Specify files as read-only

    if blueprint.test_cmd:
        command.append("--auto-test")
        command.append(f"--test-cmd={blueprint.test_cmd}")
    if blueprint.lint:
        command.append("--lint")
    if not blueprint.auto_commit:
        command.append("--no-auto-commits")
    if blueprint.verbose:
        command.append("--verbose")

    # Step 6: Handle `context_files` - Add any context files as read-only files
    for context_file in blueprint.context_files:
        command.extend(["--read", context_file])

    # Step 7: Handle `additional_args` - Append any extra arguments
    command.extend(blueprint.additional_args)

    # Step 8: Handle `message` - Write the message to a temp file if provided
    if blueprint.message:
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_message_file:
            temp_message_file.write(blueprint.message)
            temp_message_file_path = temp_message_file.name
        command.append(f"--message-file={temp_message_file_path}")  # Use the temp file path

    # Print and execute the command
    typer.echo(f"Running command: {' '.join(command)}")
    subprocess.run(command)
    
    # Step 9: Clean up the temp message file if it exists
    if os.path.exists(temp_message_file_path):
        os.remove(temp_message_file_path)