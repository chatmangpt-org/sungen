import os

import typer
from jinja2 import Environment, FileSystemLoader
from sungen.utils.dspy_tools import init_dspy, predict_type
from sungen.plugins.context.models.context_models import (
    ProjectOverview,
    ArchitectureModel,
    DevelopmentModel,
    BusinessRequirementsModel,
    QualityAssuranceModel,
    DeploymentModel,
)

app = typer.Typer(
    name="sentence",
    help="Generates comprehensive .context.md and .contextdocs.md files for software projects."
)


def generate_context_parts(input_sentence: str) -> dict:
    """Generate context parts from input sentence."""
    init_dspy()
    input_data = {"user_story": input_sentence}
    return {
        "Project Overview": predict_type(input_data, ProjectOverview),
        "Architecture Model": predict_type(input_data, ArchitectureModel),
        "Development Model": predict_type(input_data, DevelopmentModel),
        "Business Requirements": predict_type(input_data, BusinessRequirementsModel),
        "Quality Assurance": predict_type(input_data, QualityAssuranceModel),
        "Deployment Model": predict_type(input_data, DeploymentModel),
    }


def log_model_outputs(outputs: dict):
    """Log outputs for different models."""
    for model_name, model_output in outputs.items():
        typer.echo(f"{model_name} output: {model_output}")


def render_templates(outputs: dict) -> tuple:
    """Render markdown content from templates."""
    # Get the absolute path of the current file's directory
    current_dir = os.path.abspath(os.path.dirname(__file__))
    # Load Jinja environment using the absolute path
    env = Environment(loader=FileSystemLoader(current_dir))

    # Pass the outputs dictionary with the correct key
    context_md_output = env.get_template('context_md.j2').render(outputs=outputs)
    contextdocs_md_output = env.get_template('contextdocs_md.j2').render(outputs=outputs)

    return context_md_output, contextdocs_md_output


def write_output_files(output_dir: str, context_md_content: str, contextdocs_md_content: str):
    """Write rendered content to output files."""
    with open(f"{output_dir}/.context.md", "w") as context_md_file:
        context_md_file.write(context_md_content)
    with open(f"{output_dir}/.contextdocs.md", "w") as contextdocs_md_file:
        contextdocs_md_file.write(contextdocs_md_content)
    typer.echo(f"Generated .context.md and .contextdocs.md files in {output_dir}")


def main(input_sentence: str, output_dir: str = "."):
    """Main function to generate all context parts and output files."""
    outputs = generate_context_parts(input_sentence)
    log_model_outputs(outputs)
    context_md_content, contextdocs_md_content = render_templates(outputs)
    write_output_files(output_dir, context_md_content, contextdocs_md_content)


@app.command()
def generate(
    input_sentence: str,
    output_dir: str = typer.Option(".", help="Output directory for generated files")
):
    """Generate .context.md and .contextdocs.md files from input sentence."""
    if not input_sentence:
        typer.echo("Error: input_sentence is required.")
        raise typer.Exit(code=1)
    main(input_sentence, output_dir)


if __name__ == '__main__':
    # Example usage
    main("I want to create a new python project")
