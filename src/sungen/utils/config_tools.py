from confz import BaseConfig, FileSource, EnvSource, validate_all_configs
from pydantic import SecretStr, AnyUrl, Field
from pathlib import Path
from typing import List, Dict, Union, Optional
import typer
import os

# Define the name of the application for which we're storing configurations
APP_NAME = "sungen"


def get_app_config_dir() -> Path:
    """
    Get the appropriate directory to store configuration files for the application.

    Returns:
        Path: The path to the configuration directory.
    """
    # Get the application directory based on the OS
    app_dir = Path(typer.get_app_dir(APP_NAME))

    # Ensure the directory exists
    if not app_dir.exists():
        app_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created configuration directory at: {app_dir}")

    return app_dir


def get_config_file_path(file_name: str = "sungen.yaml") -> Path:
    """
    Get the full path to a configuration file within the application directory.

    Args:
        file_name (str): The name of the configuration file.

    Returns:
        Path: The full path to the configuration file.
    """
    # Retrieve the configuration directory and construct the full path
    config_path = get_app_config_dir() / file_name
    return config_path


def check_config_exists(file_name: str = "sungen.yaml") -> bool:
    """
    Check if a specific configuration file exists.

    Args:
        file_name (str): The name of the configuration file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    config_path = get_config_file_path(file_name)
    exists = config_path.is_file()

    if exists:
        print(f"Configuration file '{file_name}' found at: {config_path}")
    else:
        print(f"Configuration file '{file_name}' does not exist at: {config_path}")

    return exists


def create_default_config(file_name: str = "sungen.yaml", content: Optional[str] = None) -> None:
    """
    Create a default configuration file with optional content if it doesn't exist.

    Args:
        file_name (str): The name of the configuration file.
        content (Optional[str]): The content to write to the file if it doesn't exist.
    """
    config_path = get_config_file_path(file_name)

    if not config_path.is_file():
        with open(config_path, 'w') as config_file:
            if content:
                config_file.write(content)
            print(f"Default configuration file created at: {config_path}")
    else:
        print(f"Configuration file already exists at: {config_path}")


# Extend configuration management to handle dynamic overrides
def override_config(key: str, value: Union[str, int, bool]):
    """
    Override configuration settings dynamically.

    Args:
        key (str): The configuration key to override.
        value (Union[str, int, bool]): The new value for the configuration key.
    """
    config = get_config()  # Retrieve the global configuration instance
    if hasattr(config, key):
        setattr(config, key, value)
        print(f"Configuration '{key}' set to {value}.")
    else:
        raise KeyError(f"Configuration key '{key}' not found.")


def load_configuration() -> 'SungenConfig':
    """
    Load and validate the configuration from multiple sources.

    Returns:
        SungenConfig: The loaded and validated configuration object.
    """
    try:
        # Ensure configuration directory and file
        if not check_config_exists():
            # Optional: Provide default content if needed
            create_default_config(content="default_config_key: default_value")

        # Load configuration from sources (YAML, environment)
        config = SungenConfig()
        print("Configuration loaded successfully.")
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        raise


class SungenConfig(BaseConfig):
    project_name: str = Field(default="my_project", description="Name of the Sungen project")
    author: str = Field(default="Your Name", description="Author of the project")
    author_email: str = Field(default="your.email@example.com", description="Author's email address")
    version: str = Field(default="1.0", description="Configuration version")

    # Define the source for the configuration file
    CONFIG_SOURCES = [
        FileSource(file=str(get_config_file_path("sungen.yaml"))),  # Load from YAML file
        EnvSource(prefix="SUNGEN_")  # Load from environment variables with 'SUNGEN_' prefix
    ]

    # Load and validate configuration early on
    @staticmethod
    def validate():
        validate_all_configs()
        print("All configurations validated successfully.")


# Example Usage
if __name__ == "__main__":
    # Validate configuration at startup
    SungenConfig.validate()
    # Load configuration
    config = load_configuration()
    print(f"Project Name: {config.project_name}")
