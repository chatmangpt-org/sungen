"""Template generation commands for sungen."""

import typer
import dspy
from pathlib import Path
from sungen.utils.dspy_tools import init_dspy, GPT_DEFAULT_MODEL
from sungen.utils.file_tools import templates_dir

app = typer.Typer()

class TemplateGenerationSignature(dspy.Signature):
    """Base signature for template generation."""
    prompt = dspy.InputField(desc="User prompt for template generation.")
    template_content = dspy.OutputField(desc="Generated template content.")

class ChatToolsTemplate(TemplateGenerationSignature):
    """Generate chat tools template."""

class PluginToolsTemplate(TemplateGenerationSignature):
    """Generate plugin tools template."""

class DspyToolsTemplate(TemplateGenerationSignature):
    """Generate DSPy tools template."""

class CliTemplate(TemplateGenerationSignature):
    """Generate CLI template."""

class CliToolsTemplate(TemplateGenerationSignature):
    """Generate CLI tools template."""

class ConfigTemplate(TemplateGenerationSignature):
    """Generate config template."""

class PluginCmdTemplate(TemplateGenerationSignature):
    """Generate plugin command template."""

class TestPluginCmdTemplate(TemplateGenerationSignature):
    """Generate test plugin command template."""

class TestPluginToolsTemplate(TemplateGenerationSignature):
    """Generate test plugin tools template."""

class ReadmeTemplate(TemplateGenerationSignature):
    """Generate README template."""

def generate_template(signature_class, prompt: str, output_file: str):
    """Generate a template using the given signature class and prompt."""
    lm = init_dspy(model=GPT_DEFAULT_MODEL)
    generator = dspy.ChainOfThought(signature_class)
    result = generator(prompt=prompt)
    
    output_path = Path(templates_dir()) / output_file
    with open(output_path, 'w') as f:
        f.write(result.template_content)
    
    typer.echo(f"Template generated and saved to {output_path}")

@app.command()
def chat_tools(prompt: str):
    """Generate chat tools template."""
    generate_template(ChatToolsTemplate, prompt, "utils/chat_tools.py.jinja2")

@app.command()
def plugin_tools(prompt: str):
    """Generate plugin tools template."""
    generate_template(PluginToolsTemplate, prompt, "utils/plugin_tools.py.jinja2")

@app.command()
def dspy_tools(prompt: str):
    """Generate DSPy tools template."""
    generate_template(DspyToolsTemplate, prompt, "utils/dspy_tools.py.jinja2")

@app.command()
def cli(prompt: str):
    """Generate CLI template."""
    generate_template(CliTemplate, prompt, "cli.py.jinja2")

@app.command()
def cli_tools(prompt: str):
    """Generate CLI tools template."""
    generate_template(CliToolsTemplate, prompt, "utils/cli_tools.py.jinja2")

@app.command()
def config(prompt: str):
    """Generate config template."""
    generate_template(ConfigTemplate, prompt, "config.yaml.jinja2")

@app.command()
def plugin_cmd(prompt: str):
    """Generate plugin command template."""
    generate_template(PluginCmdTemplate, prompt, "cmds/plugin_cmd.py.j2")

@app.command()
def test_plugin_cmd(prompt: str):
    """Generate test plugin command template."""
    generate_template(TestPluginCmdTemplate, prompt, "tests/cmds/test_plugin_cmd.py.jinja2")

@app.command()
def test_plugin_tools(prompt: str):
    """Generate test plugin tools template."""
    generate_template(TestPluginToolsTemplate, prompt, "tests/utils/plugins/test_plugin_tools.py.jinja2")

@app.command()
def readme(prompt: str):
    """Generate README template."""
    generate_template(ReadmeTemplate, prompt, "README.md.jinja2")

if __name__ == "__main__":
    app()