"""
my_interpolation_plugin Plugin
This plugin provides This
 plugin performs text interpolation..

Author: John Doe
Version: 1.0.0
"""

import typer
app = typer.Typer()

@app.command()
def example():
    """Example command for my_interpolation_plugin."""
    typer.echo("This is an example command for the my_interpolation_plugin plugin.")

def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
    parent_app.add_typer(app, name="my_interpolation_plugin")