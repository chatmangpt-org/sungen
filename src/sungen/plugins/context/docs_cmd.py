# import os
# import typer
# from jinja2 import Environment, FileSystemLoader
# from sungen.plugins.context.models.contextdocs_models import ContextDocsModel, DocumentationSource, Resource
# from sungen.utils.dspy_tools import extract_external_links
#
# app = typer.Typer(
#     name="contextdocs",
#     help="Generates a .contextdocs.md file from an existing .context.md file."
# )
#
#
# def extract_external_resources_from_context_md(context_md_path: str) -> ContextDocsModel:
#     """Extract external resources from the .context.md file to create .contextdocs content."""
#     # Read the content of the .context.md file
#     with open(context_md_path, "r") as context_md_file:
#         content = context_md_file.read()
#
#     # Use a utility function to extract external links and other references
#     external_links = extract_external_links(content)
#
#     # Convert extracted links into the format required by ContextDocsModel
#     resources = []
#     for link in external_links:
#         resources.append(Resource(title=link["title"], url=link["url"]))
#
#     # Create a documentation source entry
#     documentation_sources = [
#         DocumentationSource(
#             name="External Resources",
#             relationship="Referenced within .context.md",
#             resources=resources
#         )
#     ]
#
#     # Return the constructed ContextDocsModel
#     return ContextDocsModel(contextdocs=documentation_sources)
#
#
# def render_contextdocs_template(contextdocs_data: ContextDocsModel) -> str:
#     """Render the .contextdocs.md file from the extracted data."""
#     current_dir = os.path.abspath(os.path.dirname(__file__))
#     env = Environment(loader=FileSystemLoader(current_dir))
#
#     # Load and render the contextdocs template
#     contextdocs_md_output = env.get_template('contextdocs_md.j2').render(contextdocs=contextdocs_data)
#     return contextdocs_md_output
#
#
# def write_contextdocs_file(output_path: str, contextdocs_content: str):
#     """Write the generated .contextdocs.md content to the specified file path."""
#     with open(output_path, "w") as contextdocs_file:
#         contextdocs_file.write(contextdocs_content)
#     typer.echo(f"Generated .contextdocs.md file at {output_path}")
#
#
# @app.command()
# def create_contextdocs(context_md_path: str, output_dir: str = typer.Option(".", help="Output directory for the generated .contextdocs.md file")):
#     """Command to create a .contextdocs.md file from an existing .context.md file."""
#     if not os.path.exists(context_md_path):
#         typer.echo("Error: .context.md file not found.")
#         raise typer.Exit(code=1)
#
#     # Extract external resources from the provided .context.md file
#     contextdocs_data = extract_external_resources_from_context_md(context_md_path)
#
#     # Render the .contextdocs.md file content
#     contextdocs_md_content = render_contextdocs_template(contextdocs_data)
#
#     # Write the .contextdocs.md file to the output directory
#     output_path = os.path.join(output_dir, ".contextdocs.md")
#     write_contextdocs_file(output_path, contextdocs_md_content)
#
#
# if __name__ == "__main__":
#     app()
