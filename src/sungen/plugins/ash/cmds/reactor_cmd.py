# import typer
# from pathlib import Path
# from typing import List, Optional
# from pydantic import parse_raw_as
# from sungen.utils.chat_tools import chatbot
# from sungen.utils.file_tools import write_file, read_file
# from sungen.plugins.ash.reactor_models import Reactor, ReactorStep, ReactorInput, ReactorOutput
# from jinja2 import Environment, FileSystemLoader
#
# app = typer.Typer()
#
# def generate_reactor_code(reactor: Reactor) -> str:
#     """Generate Elixir code for an Ash Reactor using the Jinja2 template."""
#     template_dir = Path(__file__).parent.parent / "templates"
#     env = Environment(loader=FileSystemLoader(str(template_dir)))
#     template = env.get_template("reactor.j2")
#     return template.render(reactor=reactor)
#
# @app.command()
# def create_reactor(
#     name: str = typer.Option(..., help="Name of the reactor"),
#     resources: List[str] = typer.Option(..., help="List of resources involved in the reactor"),
#     output_dir: Path = typer.Option("./lib/reactors", help="Output directory for generated reactor code"),
# ):
#     """Create a new Ash Reactor."""
#     typer.echo(f"Creating reactor '{name}' involving resources: {', '.join(resources)}")
#
#     # Use LLM to design the reactor
#     prompt = f"""
#     Design a reactor named '{name}' using Ash Reactor that involves the following resources: {', '.join(resources)}.
#
#     The reactor should:
#     1. Define appropriate inputs
#     2. Create a series of steps that interact with the given resources
#     3. Specify any wait conditions between steps
#     4. Define the outputs of the reactor
#
#     Provide the output as a JSON object representing the Reactor structure, following this schema:
#     {{
#         "name": "string",
#         "inputs": [{{ "name": "string", "type": "string" }}],
#         "steps": [{{
#             "name": "string",
#             "type": "string",
#             "resource": "string",
#             "action": "string",
#             "arguments": {{}},
#             "inputs": {{}},
#             "wait_for": ["string"]
#         }}],
#         "outputs": [{{ "name": "string", "source": "string or object" }}]
#     }}
#     """
#
#     reactor_json = chatbot(prompt, context="Ash Reactor design")
#     reactor = parse_raw_as(Reactor, reactor_json)
#
#     # Generate Elixir code for the Reactor
#     reactor_code = generate_reactor_code(reactor)
#
#     # Write the generated code to a file
#     output_file = output_dir / f"{name.lower()}_reactor.ex"
#     write_file(output_file, reactor_code)
#
#     typer.echo(f"Reactor '{name}' created successfully. Code written to {output_file}")
#
# @app.command()
# def list_reactors(
#     output_dir: Path = typer.Option("./lib/reactors", help="Directory containing reactor files"),
# ):
#     """List all available reactors."""
#     reactors = list(output_dir.glob("*_reactor.ex"))
#     if reactors:
#         typer.echo("Available reactors:")
#         for reactor in reactors:
#             typer.echo(f"- {reactor.stem.replace('_reactor', '')}")
#     else:
#         typer.echo("No reactors found.")
#
# @app.command()
# def analyze_reactor(
#     name: str = typer.Option(..., help="Name of the reactor to analyze"),
#     output_dir: Path = typer.Option("./lib/reactors", help="Directory containing reactor files"),
# ):
#     """Analyze a reactor and provide insights."""
#     reactor_file = output_dir / f"{name.lower()}_reactor.ex"
#     if not reactor_file.exists():
#         typer.echo(f"Reactor '{name}' not found.")
#         return
#
#     reactor_code = read_file(reactor_file)
#
#     prompt = f"""
#     Analyze the following Ash Reactor:
#
#     {reactor_code}
#
#     Provide insights on:
#     1. The overall structure and purpose of the reactor
#     2. The resources and actions involved
#     3. Any potential bottlenecks or areas for optimization
#     4. Suggestions for error handling or resilience improvements
#     5. Any other relevant observations or recommendations
#     """
#
#     analysis = chatbot(prompt, context="Ash Reactor analysis")
#     typer.echo(f"Analysis of reactor '{name}':")
#     typer.echo(analysis)
#
# @app.command()
# def optimize_reactor(
#     name: str = typer.Option(..., help="Name of the reactor to optimize"),
#     output_dir: Path = typer.Option("./lib/reactors", help="Directory containing reactor files"),
# ):
#     """Optimize an existing reactor."""
#     reactor_file = output_dir / f"{name.lower()}_reactor.ex"
#     if not reactor_file.exists():
#         typer.echo(f"Reactor '{name}' not found.")
#         return
#
#     reactor_code = read_file(reactor_file)
#
#     prompt = f"""
#     Optimize the following Ash Reactor:
#
#     {reactor_code}
#
#     Provide an optimized version of the reactor, considering:
#     1. Performance improvements
#     2. Better error handling and resilience
#     3. Clearer structure and readability
#     4. Any other relevant optimizations
#
#     Return the optimized Elixir code for the Reactor.
#     """
#
#     optimized_code = chatbot(prompt, context="Ash Reactor optimization")
#
#     # Write the optimized code to a file
#     optimized_file = output_dir / f"{name.lower()}_reactor_optimized.ex"
#     write_file(optimized_file, optimized_code)
#
#     typer.echo(f"Optimized reactor '{name}' created. Code written to {optimized_file}")
#
# @app.command()
# def generate_reactor_tests(
#     name: str = typer.Option(..., help="Name of the reactor to generate tests for"),
#     output_dir: Path = typer.Option("./test/reactors", help="Output directory for generated test code"),
# ):
#     """Generate tests for an Ash Reactor."""
#     reactor_file = Path(f"./lib/reactors/{name.lower()}_reactor.ex")
#     if not reactor_file.exists():
#         typer.echo(f"Reactor '{name}' not found.")
#         return
#
#     reactor_code = read_file(reactor_file)
#
#     prompt = f"""
#     Generate ExUnit tests for the following Ash Reactor:
#
#     {reactor_code}
#
#     The tests should cover:
#     1. Happy path scenarios
#     2. Error handling and edge cases
#     3. Different input combinations
#     4. Mocking of resource actions where appropriate
#
#     Return the Elixir code for the ExUnit tests.
#     """
#
#     test_code = chatbot(prompt, context="Ash Reactor test generation")
#
#     # Write the test code to a file
#     test_file = output_dir / f"{name.lower()}_reactor_test.exs"
#     write_file(test_file, test_code)
#
#     typer.echo(f"Tests for reactor '{name}' generated. Code written to {test_file}")
#
# if __name__ == "__main__":
#     app()