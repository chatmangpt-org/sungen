import os
import shutil

import dspy
import typer
from pathlib import Path
from jinja2 import Template
from typing import Optional
import inflection
import json

from sungen.lm.cerebras import Cerebras
from sungen.utils.file_tools import plugins_dir
from sungen.utils.plugin_tools import (
    PluginSettings,
    DependencyConfig,
    CompatibilityConfig,
    MarketplaceConfig,
    SupportConfig,
    AdvancedOptionsConfig,
    create_plugin_yaml,
    load_plugin_config,
)
from sungen.utils.chat_tools import chatbot
from sungen.utils.dspy_tools import init_dspy, init_ol, GPT_DEFAULT_MODEL
from io import StringIO

from sungen.utils.str_tools import pythonic_str

app = typer.Typer(name="plugin")

# Templates for plugin files
plugin_py_template = '''"""
{{ plugin_name }} Plugin
This plugin provides {{ plugin_description }}.

Author: {{ author }}
Version: {{ version }}
"""

import typer


app = typer.Typer(name="{{ plugin_name }}", help="{{ plugin_description }}")


@app.command()
def example():
    """
    Example command for {{ plugin_name }}.
    
    Usage:
    sungen {{ plugin_name }} example
    """
    typer.echo("This is an example command for the {{ plugin_name }} plugin.")


def check_installation():
    """
    Check if {{ plugin_name }} dependencies are installed and install them if not present.
    """
    try:
        import importlib.util
        import subprocess
        import sys


        if importlib.util.find_spec("{{ plugin_name }}_dep") is None:
            print("{{ plugin_name }}_dep is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "{{ plugin_name }}_dep"])
            print("{{ plugin_name }}_dep has been installed successfully.")

    except Exception as e:
        print(f"Error during library installation check")
        raise e


def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
    # check_installation()

    parent_app.add_typer(app, name="{{ plugin_name }}")
'''


def create_directory_structure(plugin_name: str, base_dir: Optional[Path] = None) -> Path:
    """Create the directory structure for a new plugin."""
    pythonic_name = inflection.underscore(plugin_name)
    if base_dir is None:
        base_dir = Path.cwd() / "src" / "plugins"
    base_path = base_dir / pythonic_name
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path


def render_template(template: str, **kwargs) -> str:
    """Render a template using Jinja2."""
    return Template(template).render(**kwargs)


def write_file(filepath: Path, content: str) -> None:
    """Write content to a file."""
    filepath.write_text(content)


def generate_plugin_files(plugin_settings: PluginSettings, base_dir: Optional[Path] = None) -> None:
    """Generates the necessary files for a new plugin."""
    base_path = create_directory_structure(plugin_settings.name, base_dir)
    pythonic_name = inflection.underscore(plugin_settings.name)

    # Render the Python plugin file
    plugin_py_content = render_template(
        plugin_py_template,
        plugin_name=plugin_settings.name,
        plugin_description=plugin_settings.description,
        author=plugin_settings.author,
        version=plugin_settings.version
    )
    write_file(base_path / f"{pythonic_name}_plugin.py", plugin_py_content)

    # Create the YAML configuration file
    create_plugin_yaml(plugin_settings, str(base_path / f"plugin.yaml"))

    # Create an empty __init__.py file
    write_file(base_path / "__init__.py", "")


def modify_files(target_path: Path, plugin_name: str) -> None:
    """
    Modify or add necessary files in the target project after migration.

    Args:
        target_path (Path): The path where the plugins have been copied.
        plugin_name (str): The name of the plugin being migrated.
    """
    try:
        # Example: Update or add necessary files in the target project
        plugin_file = target_path / f"{plugin_name}_plugin.py"

        if plugin_file.exists():
            # Read the content to modify it if necessary
            content = plugin_file.read_text()
            # Modify the content if needed
            # This is a placeholder modification
            content += "\n# Additional configurations or custom code here\n"
            plugin_file.write_text(content)

        # Add or modify any other files as needed
        typer.echo(f"Modified files in {target_path} for plugin '{plugin_name}'.")
    except Exception as e:
        typer.echo(f"Error modifying files: {str(e)}")
        raise e

def copy_plugin_files(source_plugin_path: Path, target_plugin_path: Path) -> None:
    """
    Copy plugin files from the source to the target directory.

    Args:
        source_plugin_path (Path): The source directory of the plugins.
        target_plugin_path (Path): The target directory where the plugins will be moved.
    """
    try:
        if not target_plugin_path.exists():
            target_plugin_path.mkdir(parents=True)

        for item in source_plugin_path.iterdir():
            s = source_plugin_path / item
            d = target_plugin_path / item.name

            if s.is_dir():
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        typer.echo(f"Successfully migrated plugins from {source_plugin_path} to {target_plugin_path}.")
    except Exception as e:
        typer.echo(f"Error during plugin migration: {str(e)}")
        raise e

@app.command()
def migrate(
    target_projects: list[str] = typer.Argument(..., help="List of paths to the target projects"),
    local_plugins_path: Path = typer.Option(Path("src/sungen/plugins"), help="Path to the local plugins directory"),
    remove_old: bool = typer.Option(False, "--remove-old", help="Remove old plugin files after migration"),
):
    """
    Migrate plugins from the local development directory to specified target projects.

    Args:
        target_projects (list[str]): Paths to the target project directories.
        local_plugins_path (Path): The source directory containing the local plugins.
        remove_old (bool): Whether to remove old plugin files after migration.
    """
    if not local_plugins_path.exists() or not local_plugins_path.is_dir():
        typer.echo(f"Local plugins path '{local_plugins_path}' does not exist or is not a directory.")
        raise typer.Exit(code=1)

    for project_path in target_projects:
        target_path = Path(project_path) / "src" / "sungen" / "plugins"

        # Copy the plugin files to the target directory
        copy_plugin_files(local_plugins_path, target_path)

        # Get all plugins from the local path and modify their target versions
        for plugin_dir in local_plugins_path.iterdir():
            if plugin_dir.is_dir():
                modify_files(target_path / plugin_dir.name, plugin_dir.name)

        if remove_old:
            shutil.rmtree(local_plugins_path)
            typer.echo(f"Old plugins removed from {local_plugins_path}.")


@app.command(name="create")
def create_plugin(
        plugin_name: str = typer.Option(..., prompt=True, help="Name of the plugin"),
        description: str = typer.Option(..., prompt=True, help="Description of the plugin"),
        author: str = typer.Option(..., prompt=True, help="Author of the plugin"),
        version: str = typer.Option("1.0.0", prompt=True, help="Version of the plugin"),
        license: str = typer.Option("MIT", prompt=True, help="License for the plugin"),
        min_sungen_version: Optional[str] = typer.Option("1.0.0", help="Minimum compatible Sungen version"),
        max_sungen_version: Optional[str] = typer.Option("2.0.0", help="Maximum compatible Sungen version"),
        base_dir: Optional[Path] = typer.Option(None, help="Base directory for plugin creation"),
):
    """
    CLI Command: Creates a new plugin with the specified name and metadata.

    sungen plugin create --plugin-name "Interpolation" --description "This plugin performs text interpolation." --author "Sean Chatman" --version "1.0.0" --license "MIT" --min-sungen-version "1.0.0" --max-sungen-version "2.0.0"
    """
    pythonic_name = inflection.underscore(plugin_name)

    if base_dir is None:
        base_dir = plugins_dir()

    plugin_settings = PluginSettings(
        name=pythonic_name,
        short_name=pythonic_name[:3],
        version=version,
        description=description,
        author=author,
        source=f"https://github.com/sungen/{pythonic_name}",
        license=license,
        tags=[pythonic_name],
        settings={
            "default_marketplace": "https://marketplace.sungen.com",
            "cache_timeout": 300,
            "auto_update_check": True,
            "log_level": "INFO",
            "retry_count": 3,
            "connection_timeout": 30,
            "backup_before_update": True,
        },
        dependencies=[
            DependencyConfig(plugin="core", version=">=1.0.0"),
        ],
        compatibility=CompatibilityConfig(
            min_sungen_version=min_sungen_version,
            max_sungen_version=max_sungen_version
        ),
        marketplace=MarketplaceConfig(
            featured=False,
            category="Utilities",
            keywords=[pythonic_name]
        ),
        support=SupportConfig(
            documentation_url=f"https://docs.sungen.com/{pythonic_name}",
            issues_url=f"https://github.com/sungen/{pythonic_name}/issues",
            contact_email="support@sungen.com"
        ),
        advanced=AdvancedOptionsConfig(
            parallel_install=True,
            secure_downloads=True,
            sandbox_mode=False
        )
    )

    generate_plugin_files(plugin_settings, base_dir)
    typer.echo(f"Plugin '{plugin_name}' created successfully!")


class GeneratePluginInfo(dspy.Signature):
    """
    Generate the name and description for a plugin based on the provided prompt.
    """

    prompt = dspy.InputField(desc="Text prompt containing details or requirements for the plugin.")

    reasoning = dspy.OutputField(desc="Brief rationale for the plugin's design.")
    plugin_name = dspy.OutputField(desc="A concise name for the plugin (2 words, <8 chars).")
    plugin_description = dspy.OutputField(desc="A brief description of the plugin's purpose and functionality.")


default_author: str | None = os.getenv("PLUGIN_AUTHOR", None)
do_prompt = os.getenv("PLUGIN_AUTHOR", None) is None


@app.command(name="prompt")
def _prompt(
        prompt: str = typer.Argument(..., help="Prompt describing the functionality and purpose of the plugin."),
        author: str = typer.Option(
            default=default_author,
            prompt=do_prompt,
            help="Author of the plugin"
        ),
        base_dir: Optional[Path] = typer.Option(plugins_dir(), help="Base directory for plugin creation")
):
    """
    CLI Command: Generate a new plugin based on a prompt

    Example:
    sungen generate-plugin --prompt "Plugin that performs advanced text interpolation for dynamic content." --author "John Doe"
    """
    # Your existing code logic
    # Step 1: Create an instance of the GeneratePluginInfo Signature class

    # Step 2: Use the DSPy Predictor to get the plugin name and description
    init_dspy(lm_class=Cerebras, max_tokens=2000)

    predictor = dspy.Predict(GeneratePluginInfo)
    output = predictor(prompt=prompt)

    # Step 3: Extract generated plugin name and description
    plugin_name = pythonic_str(output.plugin_name)
    plugin_description = output.plugin_description

    # Define default values for other plugin settings
    version = "1.0.0"
    license_type = "MIT"
    min_sungen_version = "1.0.0"
    max_sungen_version = "2.0.0"

    # Step 4: Generate Plugin Settings
    plugin_settings = PluginSettings(
        name=plugin_name,
        short_name=plugin_name[:3],
        version=version,
        description=plugin_description,
        author=author,
        source=f"https://github.com/sungen/{inflection.underscore(plugin_name)}",
        license=license_type,
        tags=[plugin_name],
        settings={
            "default_marketplace": "https://marketplace.sungen.com",
            "cache_timeout": 300,
            "auto_update_check": True,
            "log_level": "INFO",
            "retry_count": 3,
            "connection_timeout": 30,
            "backup_before_update": True,
        },
        dependencies=[
            DependencyConfig(plugin="core", version=">=1.0.0"),
        ],
        compatibility=CompatibilityConfig(
            min_sungen_version=min_sungen_version,
            max_sungen_version=max_sungen_version
        ),
        marketplace=MarketplaceConfig(
            featured=False,
            category="Utilities",
            keywords=[inflection.underscore(plugin_name)]
        ),
        support=SupportConfig(
            documentation_url=f"https://docs.sungen.com/{inflection.underscore(plugin_name)}",
            issues_url=f"https://github.com/sungen/{inflection.underscore(plugin_name)}/issues",
            contact_email="support@sungen.com"
        ),
        advanced=AdvancedOptionsConfig(
            parallel_install=True,
            secure_downloads=True,
            sandbox_mode=False
        )
    )

    # Step 5: Generate Plugin Files
    generate_plugin_files(plugin_settings, base_dir)
    typer.echo(f"Plugin '{plugin_name}' created successfully!")


@app.command(name="chat")
def chat(
    question: str = typer.Argument(..., help="Question for the chatbot about plugin_cmd.py"),
    model: str = typer.Option(GPT_DEFAULT_MODEL, help="Model to use for the chatbot (e.g., gpt-4-turbo, qwen2:instruct)")
):
    """
    CLI Command: Chat about the plugin_cmd.py file using the specified model.
    """
    # Get the content of plugin_cmd.py
    plugin_cmd_path = Path(__file__)
    plugin_cmd_content = plugin_cmd_path.read_text()
    

    
    # Prepare the context for the chatbot
    context = f"""
    File: plugin_cmd.py
    
    File Content:
    {plugin_cmd_content}
    """
    
    # Start the chat session
    typer.echo(f"Starting chat session about plugin_cmd.py using model: {model}...")
    history = chatbot(question=question, context=context, model=model)
    
    while True:
        user_input = typer.prompt("You", default="exit")
        if user_input.lower() in ['exit', 'quit', 'q']:
            break
        history = chatbot(question=user_input, context=context, history=history, model=model)

    typer.echo("Chat session ended.")


if __name__ == "__main__":
    app()
