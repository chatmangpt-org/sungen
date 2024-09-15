import os
import typer
import yaml
from typing import List

app = typer.Typer(
    name="blueprint",
    help="Plugin for creating, managing, and executing blueprints in Aider."
)

def create_blueprint_logic(
        blueprint_name: str, description: str, files_to_create: List[str], files_to_edit: List[str],
        read_only_files: List[str], model: str, auto_test: bool, lint: bool,
        auto_commit: bool, verbose: bool, additional_args: List[str], message: str):
    """
    Logic for creating a new blueprint.
    """
    blueprint = AiderBlueprint(
        module_name=blueprint_name,
        description=description,
        files_to_create=files_to_create,
        files_to_edit=files_to_edit,
        read_only_files=read_only_files,
        model=model,
        auto_test=auto_test,
        lint=lint,
        auto_commit=auto_commit,
        verbose=verbose,
        additional_args=additional_args,
        message=message
    )

    blueprint_file = f"{blueprint_name}.yml"
    blueprint.to_yaml(blueprint_file)
    typer.echo(f"Blueprint '{blueprint_name}' created and saved to {blueprint_file}.")

@app.command()
def create_blueprint(
        blueprint_name: str = typer.Argument(..., help="Name of the new blueprint"),
        description: str = typer.Option(..., help="Description of the blueprint"),
        files_to_create: List[str] = typer.Option([], help="List of files to be created"),
        files_to_edit: List[str] = typer.Option([], help="List of files to be edited"),
        read_only_files: List[str] = typer.Option([], help="List of read-only files"),
        model: str = typer.Option("gpt-4o-mini", help="AI model to use"),
        auto_test: bool = typer.Option(True, help="Enable or disable automatic testing"),
        lint: bool = typer.Option(True, help="Enable or disable linting"),
        auto_commit: bool = typer.Option(False, help="Enable or disable automatic commits."),
        verbose: bool = typer.Option(False, help="Enable or disable verbose output."),
        additional_args: List[str] = typer.Option([], help="Additional arguments for Aider"),
        message: str = typer.Option("", help="Custom message to use for Aider")
):
    """
    Create a new blueprint.
    """
    create_blueprint_logic(
        blueprint_name, description, files_to_create, files_to_edit, read_only_files,
        model, auto_test, lint, auto_commit, verbose, additional_args, message
    )

if __name__ == "__main__":
    app()
