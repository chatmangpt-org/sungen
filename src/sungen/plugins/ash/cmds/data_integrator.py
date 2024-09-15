# import typer
# from typing import List, Optional
# from pathlib import Path
# from sungen.utils.chat_tools import chatbot
# import json
#
# app = typer.Typer()
#
# @app.command()
# def generate_code(
#     resource_name: str,
#     attributes: List[str] = typer.Option([], "--attr", "-a", help="Resource attributes in the format 'name:type'"),
#     output_dir: Path = typer.Option("./lib", help="Output directory for generated code"),
# ):
#     """Generate Ash resource code."""
#     code = chatbot(f"Generate Elixir code for an Ash resource named {resource_name} with attributes {attributes}")
#     file_path = output_dir / f"{resource_name.lower()}.ex"
#     write_file(file_path, code)
#     return {"resource": resource_name, "file_path": str(file_path)}
#
# @app.command()
# def generate_tests(
#     resource_name: str,
#     output_dir: Path = typer.Option("./test", help="Output directory for generated tests"),
# ):
#     """Generate tests for an Ash resource."""
#     test_code = chatbot(f"Generate ExUnit tests for the Ash resource {resource_name}")
#     file_path = output_dir / f"{resource_name.lower()}_test.exs"
#     write_file(file_path, test_code)
#     return {"resource": resource_name, "test_file_path": str(file_path)}
#
# @app.command()
# def generate_docs(
#     resource_name: str,
#     output_dir: Path = typer.Option("./docs", help="Output directory for generated documentation"),
# ):
#     """Generate documentation for an Ash resource."""
#     docs = chatbot(f"Generate documentation for the Ash resource {resource_name}")
#     file_path = output_dir / f"{resource_name.lower()}.md"
#     write_file(file_path, docs)
#     return {"resource": resource_name, "doc_file_path": str(file_path)}
#
# @app.command()
# def integrate_data_source(
#     source_type: str = typer.Option(..., help="Type of data source (e.g., 'postgres', 'mysql', 'api')"),
#     connection_string: str = typer.Option(..., help="Connection string or URL for the data source"),
#     resource_name: str = typer.Option(..., help="Name of the Ash resource to create"),
# ):
#     """Integrate an external data source with Ash Studio."""
#     config = chatbot(f"Generate Ash configuration for integrating a {source_type} data source for resource {resource_name}")
#     file_path = Path(f"./config/{resource_name.lower()}_data_source.exs")
#     write_file(file_path, config)
#     return {"resource": resource_name, "data_source_config": str(file_path)}
#
# @app.command()
# def generate_migration(
#     resource_name: str,
#     output_dir: Path = typer.Option("./priv/repo/migrations", help="Output directory for generated migration"),
# ):
#     """Generate a migration for an Ash resource."""
#     migration_code = chatbot(f"Generate an Ecto migration for the Ash resource {resource_name}")
#     timestamp = typer.prompt("Enter the migration timestamp (YYYYMMDDHHMMSS)")
#     file_path = output_dir / f"{timestamp}_create_{resource_name.lower()}.exs"
#     write_file(file_path, migration_code)
#     return {"resource": resource_name, "migration_file_path": str(file_path)}
#
# @app.command()
# def generate_api_endpoint(
#     resource_name: str,
#     api_type: str = typer.Option("json_api", help="Type of API to generate (json_api or graphql)"),
#     output_dir: Path = typer.Option("./lib/api", help="Output directory for generated API code"),
# ):
#     """Generate API endpoint for an Ash resource."""
#     api_code = chatbot(f"Generate {api_type.upper()} API endpoint for Ash resource {resource_name}")
#     file_path = output_dir / f"{resource_name.lower()}_api.ex"
#     write_file(file_path, api_code)
#     return {"resource": resource_name, "api_type": api_type, "api_file_path": str(file_path)}
#
# @app.command()
# def generate_policy(
#     resource_name: str,
#     actions: List[str] = typer.Option([], "--action", "-a", help="Actions to include in the policy"),
#     output_dir: Path = typer.Option("./lib/policies", help="Output directory for generated policy"),
# ):
#     """Generate a policy for an Ash resource."""
#     policy_code = chatbot(f"Generate Ash policy for resource {resource_name} with actions {actions}")
#     file_path = output_dir / f"{resource_name.lower()}_policy.ex"
#     write_file(file_path, policy_code)
#     return {"resource": resource_name, "actions": actions, "policy_file_path": str(file_path)}
#
# @app.command()
# def generate_project_structure(
#     project_name: str,
#     output_dir: Path = typer.Option(".", help="Output directory for the project"),
# ):
#     """Generate a complete Ash Studio project structure."""
#     structure = {
#         "lib": {
#             f"{project_name}": {
#                 "resources": {},
#                 "policies": {},
#                 "api": {},
#             },
#         },
#         "test": {
#             "resources": {},
#             "policies": {},
#             "api": {},
#         },
#         "config": {},
#         "priv": {
#             "repo": {
#                 "migrations": {},
#             },
#         },
#         "docs": {},
#     }
#
#     def create_directory_structure(base_path, structure):
#         for key, value in structure.items():
#             path = base_path / key
#             path.mkdir(parents=True, exist_ok=True)
#             if isinstance(value, dict):
#                 create_directory_structure(path, value)
#
#     project_path = output_dir / project_name
#     create_directory_structure(project_path, structure)
#
#     # Generate basic configuration files
#     config_code = chatbot(f"Generate basic Ash Studio configuration for project {project_name}")
#     write_file(project_path / "config" / "config.exs", config_code)
#
#     return {"project_name": project_name, "project_path": str(project_path)}
#
# @app.command()
# def generate_full_resource(
#     resource_name: str,
#     attributes: List[str] = typer.Option([], "--attr", "-a", help="Resource attributes in the format 'name:type'"),
#     actions: List[str] = typer.Option([], "--action", "-c", help="Actions to include for the resource"),
#     api_type: str = typer.Option("json_api", help="Type of API to generate (json_api or graphql)"),
#     output_dir: Path = typer.Option(".", help="Output directory for the project"),
# ):
#     """Generate a complete Ash resource with tests, documentation, API endpoint, and policy."""
#     results = {}
#
#     results["resource"] = generate_code(resource_name, attributes, output_dir / "lib" / "resources")
#     results["tests"] = generate_tests(resource_name, output_dir / "test" / "resources")
#     results["docs"] = generate_docs(resource_name, output_dir / "docs")
#     results["api"] = generate_api_endpoint(resource_name, api_type, output_dir / "lib" / "api")
#     results["policy"] = generate_policy(resource_name, actions, output_dir / "lib" / "policies")
#     results["migration"] = generate_migration(resource_name, output_dir / "priv" / "repo" / "migrations")
#
#     # Generate a summary JSON file
#     summary = {
#         "resource_name": resource_name,
#         "attributes": attributes,
#         "actions": actions,
#         "api_type": api_type,
#         "generated_files": {
#             "resource": results["resource"]["file_path"],
#             "tests": results["tests"]["test_file_path"],
#             "docs": results["docs"]["doc_file_path"],
#             "api": results["api"]["api_file_path"],
#             "policy": results["policy"]["policy_file_path"],
#             "migration": results["migration"]["migration_file_path"],
#         }
#     }
#
#     summary_file = output_dir / f"{resource_name}_summary.json"
#     with open(summary_file, "w") as f:
#         json.dump(summary, f, indent=2)
#
#     return {"resource_name": resource_name, "summary_file": str(summary_file)}
#
# if __name__ == "__main__":
#     app()