"""
 Plugin
This plugin provides Test Description.

Author: Test Author
Version: 1.0.0
"""

import typer
app = typer.Typer()

@app.command()
def example():
    """Example command for ."""
    typer.echo("This is an example command for the  plugin.")

def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
    parent_app.add_typer(app, name="")