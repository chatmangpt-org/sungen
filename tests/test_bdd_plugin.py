# import pytest
# import subprocess
# from pathlib import Path
# from typer.testing import CliRunner
# from sungen.plugins.bdd.bdd_plugin import app

# runner = CliRunner()

# def test_generate_gherkin():
#     """Test the generation of a Gherkin feature file."""
#     prompt = "As a user, I want to log in"
#     result = runner.invoke(app, ["create", prompt, "--output-file", "features/test_login.feature", "--generate-code"])

#     assert result.exit_code == 0
#     assert "Generated Gherkin file" in result.output
#     assert Path("features/test_login.feature").exists()

# def test_generate_test_code():
#     """Test the generation of the corresponding test code."""
#     feature_file = Path("features/test_login.feature")
#     output_dir = Path("tests/functional")

#     # Ensure the feature file exists before generating test code
#     if feature_file.exists():
#         result = runner.invoke(app, ["gen", str(feature_file), "--output-dir", str(output_dir)])

#         assert result.exit_code == 0
#         assert "Generated test code saved to" in result.output
#         assert Path(output_dir / "test_test_login.py").exists()
#     else:
#         pytest.fail("Feature file was not created.")

# @pytest.fixture(scope="module", autouse=True)
# def cleanup():
#     """Cleanup generated files after tests."""
#     yield
#     # Remove generated files after tests
#     for path in ["features/test_login.feature", "tests/functional/test_test_login.py"]:
#         try:
#             Path(path).unlink()
#         except FileNotFoundError:
#             pass