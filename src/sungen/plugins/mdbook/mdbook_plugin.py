"""
mdbook Plugin
This plugin provides A plugin for mdbook that bundles related chapters and sections into a single, downloadable PDF or EPUB file, making it easier to share and distribute book content..

Author: Sean Chatman
Version: 1.0.0
"""

import typer
app = typer.Typer(name="mdbook")

@app.command()
def example():
    """Example command for mdbook."""
    typer.echo("This is an example command for the mdbook plugin.")

def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
    parent_app.add_typer(app, name="mdbook", help="This is a mdbook plugin that generates entire books with LLMs.")