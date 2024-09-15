# import typer
# from pathlib import Path
# from typing import List, Dict, Any
# from pydantic import BaseModel
# from sungen.utils.chat_tools import chatbot
# from sungen.utils.file_tools import write_file, read_file
# from sungen.plugins.ash.ash_models import AshResource, Action
# from jinja2 import Environment, FileSystemLoader
#
# app = typer.Typer()
#
# class ReactorStep(BaseModel):
#     name: str
#     type: str
#     resource: str
#     action: str
#     inputs: Dict[str, Any]
#     wait_for: List[str] = []
#
# class Reactor(BaseModel):
#     name: str
#     steps: List[ReactorStep]
#     inputs: Dict[str, Any] = {}
#     outputs: List[str] = []
#
# def generate_reactor_code(reactor: Reactor) -> str:
#     """Generate Elixir code for an Ash Reactor using the Jinja2 template."""
#     template_dir = Path(__file__).parent.parent / "templates"
#     env = Environment(loader=FileSystemLoader(str(template_dir)))
#     template = env.get_template("reactor.j2")
#     return template.render(reactor=reactor)
#
# def generate_reactor_steps(steps: List[ReactorStep]) -> str:
#     """Generate Elixir code for Reactor steps."""
#     step_code = []
#     for step in steps:
#         inputs = ", ".join(f"{k}: {v}" for k, v in step.inputs.items())
#         wait_for = f"wait_for {', '.join(step.wait_for)}\n  " if step.wait_for else ""
#         step_code.append(f"""
#   {step.type} :{step.name}, {step.resource} do
#     {wait_for}action :{step.action}
#     inputs %{{
#       {inputs}
#     }}
#   end
# """)
#     return "\n".join(step_code)
#
# def generate_reactor_outputs(outputs: List[str]) -> str:
#     """Generate Elixir code for Reactor outputs."""
#     return f"return {', '.join(f':{output}' for output in outputs)}"
#
# @app.command()
# def create_workflow(
#     name: str = typer.Option(..., help="Name of the workflow"),
#     resources: List[str] = typer.Option(..., help="List of resources involved in the workflow"),
#     output_dir: Path = typer.Option("./lib/workflows", help="Output directory for generated workflow code"),
# ):
#     """Create a new workflow using Ash Reactor."""
#     typer.echo(f"Creating workflow '{name}' involving resources: {', '.join(resources)}")
#
#     # Use LLM to design the workflow
#     prompt = f"""
#     Design a workflow named '{name}' using Ash Reactor that involves the following resources: {', '.join(resources)}.
#
#     The workflow should:
#     1. Define appropriate inputs
#     2. Create a series of steps that interact with the given resources
#     3. Specify any wait conditions between steps
#     4. Define the outputs of the workflow
#
#     Provide the output as a JSON object representing the Reactor structure.
#     """
#
#     reactor_json = chatbot(prompt, context="Ash Reactor workflow design")
#     reactor = Reactor.parse_raw(reactor_json)
#
#     # Generate Elixir code for the Reactor
#     reactor_code = generate_reactor_code(reactor)
#
#     # Write the generated code to a file
#     output_file = output_dir / f"{name.lower()}_workflow.ex"
#     write_file(output_file, reactor_code)
#
#     typer.echo(f"Workflow '{name}' created successfully. Code written to {output_file}")
#
# @app.command()
# def list_workflows(
#     output_dir: Path = typer.Option("./lib/workflows", help="Directory containing workflow files"),
# ):
#     """List all available workflows."""
#     workflows = list(output_dir.glob("*_workflow.ex"))
#     if workflows:
#         typer.echo("Available workflows:")
#         for workflow in workflows:
#             typer.echo(f"- {workflow.stem.replace('_workflow', '')}")
#     else:
#         typer.echo("No workflows found.")
#
# @app.command()
# def analyze_workflow(
#     name: str = typer.Option(..., help="Name of the workflow to analyze"),
#     output_dir: Path = typer.Option("./lib/workflows", help="Directory containing workflow files"),
# ):
#     """Analyze a workflow and provide insights."""
#     workflow_file = output_dir / f"{name.lower()}_workflow.ex"
#     if not workflow_file.exists():
#         typer.echo(f"Workflow '{name}' not found.")
#         return
#
#     workflow_code = read_file(workflow_file)
#
#     prompt = f"""
#     Analyze the following Ash Reactor workflow:
#
#     {workflow_code}
#
#     Provide insights on:
#     1. The overall structure and purpose of the workflow
#     2. The resources and actions involved
#     3. Any potential bottlenecks or areas for optimization
#     4. Suggestions for error handling or resilience improvements
#     5. Any other relevant observations or recommendations
#     """
#
#     analysis = chatbot(prompt, context="Ash Reactor workflow analysis")
#     typer.echo(f"Analysis of workflow '{name}':")
#     typer.echo(analysis)
#
# @app.command()
# def optimize_workflow(
#     name: str = typer.Option(..., help="Name of the workflow to optimize"),
#     output_dir: Path = typer.Option("./lib/workflows", help="Directory containing workflow files"),
# ):
#     """Optimize an existing workflow."""
#     workflow_file = output_dir / f"{name.lower()}_workflow.ex"
#     if not workflow_file.exists():
#         typer.echo(f"Workflow '{name}' not found.")
#         return
#
#     workflow_code = read_file(workflow_file)
#
#     prompt = f"""
#     Optimize the following Ash Reactor workflow:
#
#     {workflow_code}
#
#     Provide an optimized version of the workflow, considering:
#     1. Performance improvements
#     2. Better error handling and resilience
#     3. Clearer structure and readability
#     4. Any other relevant optimizations
#
#     Return the optimized Elixir code for the Reactor.
#     """
#
#     optimized_code = chatbot(prompt, context="Ash Reactor workflow optimization")
#
#     # Write the optimized code to a file
#     optimized_file = output_dir / f"{name.lower()}_workflow_optimized.ex"
#     write_file(optimized_file, optimized_code)
#
#     typer.echo(f"Optimized workflow '{name}' created. Code written to {optimized_file}")
#
# if __name__ == "__main__":
#     app()