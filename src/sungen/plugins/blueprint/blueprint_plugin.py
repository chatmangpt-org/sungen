"""
blueprint Plugin
This plugin provides A plugin to create, manage, and execute blueprints in Aider..

Author: Sean Chatman
Version: 1.0.0
"""

import typer


app = typer.Typer(name="blueprint", help="A plugin to create, manage, and execute blueprints in Aider.")


@app.command()
def example():
    """
    Example command for blueprint.
    
    Usage:
    sungen blueprint example
    """
    typer.echo("This is an example command for the blueprint plugin.")


def check_installation():
    """
    Check if blueprint dependencies are installed and install them if not present.
    """
    try:
        import importlib.util
        import subprocess
        import sys


        if importlib.util.find_spec("blueprint_dep") is None:
            print("blueprint_dep is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "blueprint_dep"])
            print("blueprint_dep has been installed successfully.")

    except Exception as e:
        print(f"Error during library installation check")
        raise e


def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
    # check_installation()

    parent_app.add_typer(app, name="blueprint")