import typer
from pathlib import Path
from jinja2 import Template
from typing import Optional
import inflection
import json
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

app = typer.Typer()

# Templates for plugin files
plugin_py_template = '''"""
{{ plugin_name }} Plugin
This plugin provides {{ plugin_description }}.

Author: {{ author }}
Version: {{ version }}
"""

import typer
app = typer.Typer()

@app.command()
def example():
    """Example command for {{ plugin_name }}."""
    typer.echo("This is an example command for the {{ plugin_name }} plugin.")

def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
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

    sungen plugin create --plugin-name "MyInterpolationPlugin" --description "This plugin performs text interpolation." --author "John Doe" --version "1.0.0" --license "MIT" --min-sungen-version "1.0.0" --max-sungen-version "2.0.0"
    """
    pythonic_name = inflection.underscore(plugin_name)
    plugin_settings = PluginSettings(
        name=pythonic_name,
        short_name=pythonic_name[:3] ,
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
