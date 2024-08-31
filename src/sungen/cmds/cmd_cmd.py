"""Generate new sub commands or add to existing ones."""
from pathlib import Path

import typer

from sungen.typetemp.functional import render

app = typer.Typer()

subcommand_template = '''"""{{ subcommand_name }}"""
import typer


app = typer.Typer()


@app.command(name="{{ new_command_name }}")
def {{ sub_command_name }}_{{ new_command_name | underscore }}():
    """{{ new_command_name }}"""
    typer.echo("Running {{ new_command_name | underscore }} subcommand.")
    
'''


# Define the subcommand to generate subcommand dspy_modules
@app.command(
    name="new",
)
def new_command(subcommand_name: str, new_command_name: str):
    """
    Generate a new subcommand module with the given name.
    Example usage: sungen command new new_command
    """
    script_dir = Path(__file__).parent

    # Generate the filename for the new subcommand module
    filename = f"{subcommand_name}_cmd.py"
    module_path = script_dir / filename

    # Check if the existing subcommand module file exists
    if module_path.exists():
        typer.echo(f"Subcommand module '{subcommand_name}' already exists.")
        return

    # Create the subcommand module file
    with open(script_dir / filename, "w") as file:
        # You can customize the content of the module here
        source = render(subcommand_template, subcommand_name=subcommand_name, new_command_name=new_command_name)
        file.write(source)

    typer.echo(f"Subcommand module '{subcommand_name}' generated successfully!")


add_template = ''' 
@app.command(name="{{ new_command_name }}")
def {{ sub_command_name }}_{{ new_command_name | underscore }}():
    """{{ new_command_name }}"""
    typer.echo("Running {{ new_command_name | underscore }} subcommand.")

'''


@app.command(name="add")
def add_command(sub_command_name: str, new_command_name: str):
    """
    Add a new command to an existing subcommand module.
    Example usage: sungen command add existing_command new_command
    """
    script_dir = Path(__file__).parent

    # Construct the filename for the existing subcommand module
    filename = f"{sub_command_name}_cmd.py"

    # Construct the path to the existing subcommand module
    module_path = script_dir / filename

    # Check if the existing subcommand module file exists
    if not module_path.exists():
        typer.echo(f"Subcommand module '{sub_command_name}' does not exist.")
        return

    # Append the code to the existing subcommand module file
    with open(module_path, "a") as module_file:
        new_command_code = render(
            add_template,
            sub_command_name=sub_command_name,
            new_command_name=new_command_name,
        )
        module_file.write(new_command_code)

    typer.echo(
        f"New command '{new_command_name}' added to subcommand module '{sub_command_name}' successfully!"
    )

@app.command(name="bulk-new")
def bulk_new(
    base_command: str = typer.Option(..., "--base", "-b", help="Base command name for all new subcommands"),
    subcommands: str = typer.Option(..., "--subcommands", "-s", help="Comma-separated list of subcommand names to create")
):
    """
    Create multiple new subcommand dspy_modules at once.
    Example usage: sungen command bulk-new -b base_command -s subcommand1,subcommand2
    """
    subcommand_list = subcommands.split(",")  # Split the comma-separated string into a list

    # Create the base command first
    new_command(base_command, base_command)

    # Add each subcommand to the base command module
    for subcommand in subcommand_list:
        add_command(base_command, subcommand.strip())  # Use strip() to remove any extra whitespace

    typer.echo(f"Bulk creation of {len(subcommand_list)} subcommand dspy_modules completed successfully!")
