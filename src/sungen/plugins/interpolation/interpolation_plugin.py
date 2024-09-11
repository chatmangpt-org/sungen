"""
interpolation Plugin
This plugin provides This plugin performs text interpolation..

Author: Sean Chatman
Version: 1.0.0
"""

import typer
app = typer.Typer(name="interpolation")


@app.command()
def example(source_doc: str, pipeline_yaml: str, prompt: str):
    """Example command for interpolation.

    This command executes a pipeline to convert a Saltcorn ebook into a Sungen ebook format.

    Args:
        source_doc (str): The path to the source Saltcorn ebook file (e.g., 'path/to/saltcorn_ebook.epub').
        pipeline_yaml (str): The path to the YAML file defining the pipeline (e.g., 'path/to/pipeline.yaml').
        prompt (str): The prompt to guide the conversion process (e.g., 'Convert this Saltcorn ebook into a Sungen ebook format.').

    Example usage:
        $ python -m sungen.plugins.interpolation.interpolation_plugin example \
            --source_doc path/to/saltcorn_ebook.epub \
            --pipeline_yaml path/to/pipeline.yaml \
            --prompt "Convert this Saltcorn ebook into a Sungen ebook format."
    """
    # Call the execute_pipeline function with the provided arguments
    from sungen.dsl.dsl_pipeline_executor import execute_pipeline
    context = execute_pipeline(pipeline_yaml, {"source_doc": source_doc, "prompt": prompt})
    
    typer.echo("Pipeline executed with context:")
    typer.echo(context)


def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
    parent_app.add_typer(app)