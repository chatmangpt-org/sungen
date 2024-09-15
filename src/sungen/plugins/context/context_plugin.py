"""
context Plugin
This plugin provides This plugin generates comprehensive .context.md and .contextdocs.md files for software projects based on the Codebase Context Specification..

Author: Sean Chatman
Version: 1.0.0
"""
import typer
from sungen.plugins.context.sentence_cmd import app as sentence_app


app = typer.Typer(name="context", help="This plugin generates comprehensive .context.md and .contextdocs.md files for software projects based on the Codebase Context Specification.")
app.add_typer(sentence_app, name="sentence")


@app.command()
def example():
    """
    Example command for context.
    
    Usage:
    sungen context example
    """
    typer.echo("This is an example command for the context plugin.")


def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
    parent_app.add_typer(app, name="context")
