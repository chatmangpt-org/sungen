import pytest
from pathlib import Path
import inflection
from sungen.cmds.plugin_cmd import (
    create_directory_structure,
    render_template,
    write_file,
    generate_plugin_files,
    plugin_py_template,
)
from sungen.utils.plugin_tools import PluginSettings, load_plugin_config
from unittest.mock import patch, MagicMock
from sungen.utils.chat_tools import handle_global_error

@pytest.fixture
def temp_plugin_dir(tmp_path):
    """Fixture to create a temporary directory for plugin creation."""
    return tmp_path

@pytest.fixture
def mock_plugin_settings():
    """Fixture to create a mock PluginSettings object."""
    plugin_name = "TestPlugin"
    pythonic_name = inflection.underscore(plugin_name)
    return PluginSettings(
        name=plugin_name,
        short_name=pythonic_name[:3],
        version="1.0.0",
        description="A test plugin",
        author="Test Author",
        source=f"https://github.com/sungen/{pythonic_name}",
        license="MIT",
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
        dependencies=[],
        compatibility={
            "min_sungen_version": "1.0.0",
            "max_sungen_version": "2.0.0"
        },
        marketplace={
            "featured": False,
            "category": "Utilities",
            "keywords": [pythonic_name]
        },
        support={
            "documentation_url": f"https://docs.sungen.com/{pythonic_name}",
            "issues_url": f"https://github.com/sungen/{pythonic_name}/issues",
            "contact_email": "support@sungen.com"
        },
        advanced={
            "parallel_install": True,
            "secure_downloads": True,
            "sandbox_mode": False
        }
    )

def test_create_directory_structure(temp_plugin_dir):
    """Test creating the directory structure for a new plugin."""
    plugin_name = "TestPlugin"
    result = create_directory_structure(plugin_name, temp_plugin_dir)
    expected_path = temp_plugin_dir / inflection.underscore(plugin_name)
    assert result == expected_path
    assert result.exists()
    assert result.is_dir()

def test_render_template():
    """Test rendering a template with Jinja2."""
    template = "{{ name }} is {{ age }} years old."
    context = {"name": "Alice", "age": 30}
    result = render_template(template, **context)
    assert result == "Alice is 30 years old."

def test_write_file(tmp_path):
    """Test writing content to a file."""
    file_path = tmp_path / "test_file.txt"
    content = "This is a test file."
    write_file(file_path, content)
    assert file_path.exists()
    assert file_path.read_text() == content

def test_generate_plugin_files(temp_plugin_dir, mock_plugin_settings):
    """Test generating all necessary files for a new plugin."""
    generate_plugin_files(mock_plugin_settings, temp_plugin_dir)
    
    pythonic_name = inflection.underscore(mock_plugin_settings.name)
    plugin_dir = temp_plugin_dir / pythonic_name
    assert plugin_dir.exists()
    assert (plugin_dir / f"{pythonic_name}.py").exists()
    assert (plugin_dir / f"{pythonic_name}.yaml").exists()
    assert (plugin_dir / "__init__.py").exists()

def test_plugin_py_content(temp_plugin_dir, mock_plugin_settings):
    """Test the content of the generated plugin Python file."""
    generate_plugin_files(mock_plugin_settings, temp_plugin_dir)
    
    pythonic_name = inflection.underscore(mock_plugin_settings.name)
    plugin_py_path = temp_plugin_dir / pythonic_name / f"{pythonic_name}.py"
    content = plugin_py_path.read_text()
    
    assert mock_plugin_settings.name in content
    assert mock_plugin_settings.description in content
    assert mock_plugin_settings.author in content
    assert mock_plugin_settings.version in content
    assert "def example():" in content
    assert "def register_plugin(parent_app: typer.Typer):" in content

def test_plugin_yaml_content(temp_plugin_dir, mock_plugin_settings):
    """Test the content of the generated plugin YAML file."""
    generate_plugin_files(mock_plugin_settings, temp_plugin_dir)
    
    pythonic_name = inflection.underscore(mock_plugin_settings.name)
    plugin_yaml_path = temp_plugin_dir / pythonic_name / f"{pythonic_name}.yaml"
    plugin_config = load_plugin_config(str(plugin_yaml_path))
    
    assert plugin_config.name == mock_plugin_settings.name
    assert plugin_config.version == mock_plugin_settings.version
    assert plugin_config.author == mock_plugin_settings.author
    assert plugin_config.license == mock_plugin_settings.license
    assert plugin_config.compatibility.min_sungen_version == mock_plugin_settings.compatibility["min_sungen_version"]
    assert plugin_config.compatibility.max_sungen_version == mock_plugin_settings.compatibility["max_sungen_version"]

def test_chat_command(monkeypatch):
    """Test the chat command about plugin_cmd.py."""
    with patch('sungen.cmds.plugin_cmd.chatbot') as mock_chatbot, \
         patch('sungen.cmds.plugin_cmd.get_cli_help') as mock_get_cli_help, \
         patch('sungen.utils.chat_tools.init_dspy') as mock_init_dspy, \
         patch('sungen.utils.chat_tools.init_ol') as mock_init_ol:
        mock_chatbot.return_value = "Mocked chat history"
        mock_get_cli_help.return_value = "Mocked CLI help"
        mock_init_dspy.return_value = MagicMock()
        mock_init_ol.return_value = MagicMock()
        
        # Run the chat command with default model (gpt-4-turbo)
        from sungen.cmds.plugin_cmd import chat
        result = typer.run(chat, ["Tell me about plugin_cmd.py"])
        
        # Check that chatbot was called with the correct context and model
        mock_chatbot.assert_called()
        context_arg = mock_chatbot.call_args[1]['context']
        assert "File: plugin_cmd.py" in context_arg
        assert "CLI Commands:" in context_arg
        assert "Mocked CLI help" in context_arg
        assert "File Content:" in context_arg
        assert "Chatbot Capabilities and Rules:" in context_arg
        assert "Context Awareness:" in context_arg
        assert "Code Generation:" in context_arg
        assert mock_chatbot.call_args[1]['model'] == "gpt-4-turbo"
        mock_init_dspy.assert_called_once()
        mock_init_ol.assert_not_called()

        # Reset mocks
        mock_chatbot.reset_mock()
        mock_init_dspy.reset_mock()
        mock_init_ol.reset_mock()

        # Run the chat command with a non-GPT model
        result = typer.run(chat, ["Tell me about plugin_cmd.py", "--model", "qwen2:instruct"])
        
        # Check that chatbot was called with the correct model
        mock_chatbot.assert_called()
        assert mock_chatbot.call_args[1]['model'] == "qwen2:instruct"
        mock_init_dspy.assert_not_called()
        mock_init_ol.assert_called_once()

def test_get_cli_help():
    """Test the get_cli_help function."""
    mock_plugin_content = """
import typer

app = typer.Typer()

@app.command()
def hello():
    '''Say hello'''
    print("Hello, World!")

if __name__ == "__main__":
    app()
    """
    
    from sungen.cmds.plugin_cmd import get_cli_help
    
    help_output = get_cli_help(mock_plugin_content)
    assert "Usage:" in help_output
    assert "hello" in help_output
    assert "Say hello" in help_output

def test_handle_global_error():
    """Test the global error handler."""
    with patch('sungen.utils.chat_tools.init_dspy') as mock_init_dspy, \
         patch('sungen.utils.chat_tools.dspy.ChainOfThought') as mock_chain_of_thought:
        mock_init_dspy.return_value = MagicMock()
        mock_analyzer = MagicMock()
        mock_analyzer.return_value = MagicMock(
            analysis="Mocked analysis",
            fix_suggestions="Mocked fix suggestions",
            architectural_insights="Mocked architectural insights"
        )
        mock_chain_of_thought.return_value = mock_analyzer

        try:
            raise ValueError("Test error")
        except ValueError:
            error_type, error_value, tb = sys.exc_info()
            handle_global_error(error_type, error_value, tb)

        mock_init_dspy.assert_called_once()
        mock_chain_of_thought.assert_called_once()
        mock_analyzer.assert_called_once()

        # You might want to add more specific assertions here to check the output

# Add more tests as needed