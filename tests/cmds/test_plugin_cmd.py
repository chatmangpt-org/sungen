import pytest
from typer.testing import CliRunner
from pathlib import Path

from sungen.cmds.plugin_cmd import app
from sungen.utils.str_tools import pythonic_str

runner = CliRunner()


@pytest.fixture
def temp_directory(tmp_path):
    """Fixture for creating a temporary directory."""
    return tmp_path


@pytest.fixture
def plugin_name():
    """Fixture for the name of the plugin."""
    return pythonic_str("Sample Plugin")


@pytest.fixture
def plugin_description():
    """Fixture for the description of the plugin."""
    return "This is a sample plugin for testing purposes."


@pytest.fixture
def author_name():
    """Fixture for the author of the plugin."""
    return "Test Author"


@pytest.fixture
def version():
    """Fixture for the version of the plugin."""
    return "1.0.0"


def test_create_plugin_command(temp_directory, plugin_name, plugin_description, author_name, version):
    """Test the create_plugin command to ensure it generates the plugin files correctly."""
    # Prepare the CLI command arguments
    result = runner.invoke(
        app,
        [
            "create",
            "--plugin-name",
            plugin_name,
            "--description",
            plugin_description,
            "--author",
            author_name,
            "--version",
            version,
            "--license",  # Added license
            "MIT",        # Default license
            "--min-sungen-version",  # Added min_sungen_version
            "1.0.0",      # Default min_sungen_version
            "--max-sungen-version",  # Added max_sungen_version
            "2.0.0",      # Default max_sungen_version
            "--base-dir",
            str(temp_directory)
        ],
    )

    # Print the output for debugging
    print(result.output)

    # Check that the command completed successfully
    assert result.exit_code == 0, f"Command failed with output: {result.output}"

    # Check that the plugin files were created in the temporary directory
    plugin_dir = temp_directory / Path(plugin_name.lower().replace(" ", "_"))  # Ensure consistent naming
    print(f"Expected plugin directory: {plugin_dir}")  # Debugging output

    plugin_yaml_path = plugin_dir / "plugin.yaml"
    plugin_py_path = plugin_dir / f"{plugin_name.lower().replace(' ', '_')}_plugin.py"
    init_py_path = plugin_dir / "__init__.py"

    # Check for the existence of the files
    assert plugin_yaml_path.exists(), f"YAML file should be created at {plugin_yaml_path}."
    assert plugin_py_path.exists(), f"Python file for the plugin should be created at {plugin_py_path}."
    assert init_py_path.exists(), f"Empty __init__.py file should be created at {init_py_path}."


def test_plugin_yaml_content(temp_directory, plugin_name, plugin_description, author_name, version):
    """Test the content of the created plugin YAML file."""
    runner.invoke(
        app,
        [
            "create",
            "--plugin-name",
            plugin_name,
            "--description",
            plugin_description,
            "--author",
            author_name,
            "--version",
            version,
            "--base-dir",
            str(temp_directory)
        ],
    )

    # Check the contents of the plugin YAML file
    plugin_dir = temp_directory / Path(plugin_name.lower().replace(" ", "_"))
    plugin_yaml_path = plugin_dir / "plugin.yaml"

    with open(plugin_yaml_path) as f:
        yaml_content = f.read()

    assert "sample_plugin" in yaml_content, "YAML file should contain the plugin name."
    assert "1.0.0" in yaml_content, "YAML file should contain the correct version."
    assert f"{plugin_description}" in yaml_content, "YAML file should contain the plugin description."
    assert f"{author_name}" in yaml_content, "YAML file should contain the author name."


def test_plugin_py_content(temp_directory, plugin_name, plugin_description, author_name, version):
    """Test the content of the created plugin Python file."""
    runner.invoke(
        app,
        [
            "create",
            "--plugin-name",
            plugin_name,
            "--description",
            plugin_description,
            "--author",
            author_name,
            "--version",
            version,
            "--base-dir",
            str(temp_directory)
        ],
    )

    # Check the contents of the plugin Python file
    plugin_dir = temp_directory / Path(plugin_name.lower().replace(" ", "_"))
    plugin_py_path = plugin_dir / f"{plugin_name.lower().replace(' ', '_')}_plugin.py"

    with open(plugin_py_path) as f:
        py_content = f.read()

    assert plugin_name in py_content, "Python file should contain the plugin name."
    assert plugin_description in py_content, "Python file should contain the plugin description."
    assert author_name in py_content, "Python file should contain the author name."


def test_create_plugin_directory_structure(temp_directory, plugin_name, plugin_description, author_name, version):
    """Test that the create_plugin command creates the correct directory structure."""
    runner.invoke(
        app,
        [
            "create",
            "--plugin-name",
            plugin_name,
            "--description",
            plugin_description,
            "--author",
            author_name,
            "--version",
            version,
            "--base-dir",
            str(temp_directory)
        ],
    )

    # Check the directory structure
    plugin_dir = temp_directory / Path(plugin_name.lower().replace(" ", "_"))
    assert plugin_dir.exists(), "Plugin directory should be created."
    assert (plugin_dir / "__init__.py").exists(), "__init__.py file should be present in the plugin directory."


def test_create_plugin_invalid_args():
    """Test create_plugin command with invalid arguments."""
    result = runner.invoke(
        app,
        [
            "create",
            "--plugin-name",
            "",  # Invalid: Empty plugin name
            "--description",
            "Test Description",
            "--author",
            "Test Author",
            "--license",  # Added license
            "MIT",        # Default license
            "--min-sungen-version",  # Added min_sungen_version
            "1.0.0",      # Default min_sungen_version
            "--max-sungen-version",  # Added max_sungen_version
            "2.0.0",      # Default max_sungen_version
        ],
    )

    assert result.exit_code != 0, "Command should fail with invalid arguments."
