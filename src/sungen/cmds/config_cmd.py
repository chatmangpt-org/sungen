import typer
from pathlib import Path
from sungen.utils.config_tools import (
    get_app_config_dir,
    get_config_file_path,
    check_config_exists,
    create_default_config,
    load_configuration,
    SungenConfig,
    override_config,
)

# Create a Typer app for the config commands
app = typer.Typer(help="Commands to manage configurations for the CLI application.")

@app.command("show")
def show_config(file_name: str = typer.Argument("sungen.yaml", help="The configuration file name.")):
    """
    Display the current configuration settings.
    """
    if check_config_exists(file_name):
        config_path = get_config_file_path(file_name)
        print(f"Configuration file found at: {config_path}")
        config = load_configuration()
        print("Current Configuration:")
        print(config.model_dump_json(indent=2))
    else:
        print(f"Configuration file '{file_name}' does not exist. Use 'create' to generate one.")


@app.command("create")
def create_config(
    file_name: str = typer.Argument("sungen.yaml", help="The name of the configuration file to create."),
    content: str = typer.Option("", "--content", "-c", help="Default content for the new configuration file.")
):
    """
    Create a new default configuration file.
    """
    create_default_config(file_name, content)
    print(f"Configuration file '{file_name}' created.")


@app.command("update")
def update_config(
    key: str = typer.Argument(..., help="The configuration key to update."),
    value: str = typer.Argument(..., help="The new value for the configuration key.")
):
    """
    Update a specific configuration setting.
    """
    try:
        override_config(key, value)
        print(f"Configuration '{key}' updated to '{value}'.")
    except KeyError as e:
        print(f"Error: {e}")


@app.command("validate")
def validate_config():
    """
    Validate the current configuration to ensure it is correctly set up.
    """
    try:
        SungenConfig.validate()
        print("Configuration is valid.")
    except Exception as e:
        print(f"Error during validation: {e}")


@app.command("reset")
def reset_config(file_name: str = typer.Argument("sungen.yaml", help="The configuration file name to reset.")):
    """
    Reset the configuration to the default state.
    """
    config_path = get_config_file_path(file_name)
    if config_path.is_file():
        config_path.unlink()  # Delete the existing configuration file
        print(f"Configuration file '{file_name}' has been reset.")
        create_default_config(file_name)  # Create a new default configuration
    else:
        print(f"Configuration file '{file_name}' does not exist. Use 'create' to generate one.")


if __name__ == "__main__":
    app()
