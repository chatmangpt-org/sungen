import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from sungen.utils.cli_tools import load_commands

@pytest.fixture
def create_temp_commands(tmp_path):
    """
    Fixture to create temporary command files in the provided directory.
    """
    cmd_dir = tmp_path / "cmds"
    cmd_dir.mkdir()

    # Create dummy command files
    (cmd_dir / "example_cmd.py").write_text("'''An example command module.'''\n")
    (cmd_dir / "another_cmd.py").write_text("'''Another command module.'''\n")

    return cmd_dir

def test_load_commands_imports(create_temp_commands):
    """Test that load_commands correctly attempts to import modules."""
    app_mock = Mock()

    with patch('sungen.utils.cli_tools.import_module') as mock_import_module:
        load_commands(app_mock, create_temp_commands)

        # Assert import_module was called correctly
        assert mock_import_module.call_count == 2
        
        # Get the actual arguments passed to import_module
        import_calls = [call[0][0] for call in mock_import_module.call_args_list]
        
        # Check that the correct module names were attempted to be imported
        assert any('example_cmd' in call for call in import_calls)
        assert any('another_cmd' in call for call in import_calls)

        # Print the actual import calls for debugging
        print(f"Actual import calls: {import_calls}")
