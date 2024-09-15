"""
bdd Plugin CLI
This file contains only the CLI commands for the auto_bdd plugin.
"""
import dspy
import typer
from pathlib import Path
from typing import Optional
import importlib.util
import subprocess
import sys

from sungen.lm.cerebras import Cerebras
from sungen.utils.dspy_tools import init_dspy

app = typer.Typer(name="bdd")


def check_installation():
    """
    Check if pytest-bdd is installed and install it if not present.
    Also check for pytest and warn if it is missing.
    """
    try:
        if importlib.util.find_spec("pytest") is None:
            print("pytest is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
            print("pytest has been installed successfully.")

        if importlib.util.find_spec("pytest_bdd") is None:
            print("pytest-bdd is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest-bdd"])
            print("pytest-bdd has been installed successfully.")
    except Exception as e:
        print(f"Error during installation check: {str(e)}")


def generate_gherkin(prompt: str, file_path: Path) -> None:
    """
    Generate a Gherkin feature file based on a prompt.
    """
    # Initialize DSPy model
    init_dspy(lm_class=Cerebras, max_tokens=2000)

    # Use DSPy Predictor to generate Gherkin text
    class GherkinInfo(dspy.Signature):
        prompt = dspy.InputField(desc="Text prompt containing details or requirements for the Gherkin feature.")
        file_name = dspy.OutputField(desc="{{feature_file_name}}.feature (no other text)")
        gherkin_text = dspy.OutputField(desc="Generated Gherkin feature file content.")

    predictor = dspy.Predict(GherkinInfo)
    output = predictor(prompt=prompt)

    print(f"Generated Gherkin file: {output.file_name}")

    # LLM sometimes returns features/File Name: login.feature, so split on " " and take the last element
    feature_file_name = output.file_name.split(" ")[-1]

    # Ensure the tests directory exists
    tests_directory = tests_dir()
    tests_directory.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        Path(tests_directory / feature_file_name).write_text(output.gherkin_text)
    else:
        file_path.write_text(output.gherkin_text)


def run_code_generator(feature_file: Path, output_dir: Path) -> None:
    """
    Run the test code generator based on the provided Gherkin feature file.
    """
    # Ensure pytest-bdd and pytest are available
    # Removed import check here
    typer.echo(f"Running code generator for feature file: {feature_file}")
    command = f"pytest-bdd generate {feature_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check for errors in the code generation process
    if result.returncode != 0:
        raise RuntimeError(f"Error running code generator: {result.stderr}")

    # Save generated code to the output directory
    output_path = output_dir / f"test_{feature_file.stem}.py"
    with open(output_path, 'w') as test_file:
        test_file.write(result.stdout)

    typer.echo(f"Generated test code saved to {output_path}")


@app.command(name="create")
def generate_gherkin_command(
        prompt: str = typer.Argument(..., help="Prompt describing the feature or scenario to generate in Gherkin."),
        output_file: Path = typer.Option(Path("features/generated.feature"),
                                         help="Output file for the generated Gherkin feature."),
        output_dir: Optional[Path] = typer.Option(Path("features"),
                                                  help="Output directory for generated Gherkin feature."),
        generate_code: bool = typer.Option(False, help="Generate code for the feature file.")
):
    """
    CLI Command: Generate a Gherkin feature file based on a prompt.

    Usage:
        sungen bdd create "As a user, I want to log in" --output-file features/login.feature --generate-code
    """
    # Only validate input, no business logic here
    if not prompt:
        typer.echo("Prompt is required.")
        raise typer.Exit(code=1)

    try:
        generate_gherkin(prompt, output_file)

        if generate_code:
            run_code_generator(output_file, output_dir)
    except Exception as e:
        typer.echo(f"Failed to generate Gherkin feature: {str(e)}")
        raise typer.Exit(code=1)


@app.command(name="gen")
def run_code_generator_command(
        feature_file: Path = typer.Argument(..., help="Path to the Gherkin feature file."),
        output_dir: Optional[Path] = typer.Option(Path("tests/functional"),
                                                  help="Output directory for generated test code.")
):
    """
    CLI Command: Run the test code generator based on the provided Gherkin feature file.

    Usage:
        sungen bdd gen features/login.feature --output-dir tests/functional
    """
    # Only validate input, no business logic here
    if not feature_file.exists():
        typer.echo("Feature file not found.")
        raise typer.Exit(code=1)

    try:
        run_code_generator(feature_file, output_dir)
    except Exception as e:
        typer.echo(f"Failed to run code generator: {str(e)}")
        raise typer.Exit(code=1)


def register_plugin(parent_app: typer.Typer):
    """
    Register the plugin with the main application.
    """
    try:
        check_installation()
        parent_app.add_typer(app)

        if app in parent_app.registered_groups:
            raise Exception("Failed to register plugin 'bdd'")
    except Exception as e:
        print(f"Failed to register plugin 'bdd': {str(e)}")


if __name__ == "__main__":
    app()
