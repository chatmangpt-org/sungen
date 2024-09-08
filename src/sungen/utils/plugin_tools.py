from confz import BaseConfig, FileSource
from typing import List, Optional
from pathlib import Path
import yaml
import os
from importlib import import_module
import typer
import importlib.util
import sys


# Define the configuration classes for plugins using ConfZ

class DependencyConfig(BaseConfig):
    """Represents a plugin dependency."""
    plugin: str
    version: str


class CompatibilityConfig(BaseConfig):
    """Specifies compatibility requirements for the plugin."""
    min_sungen_version: str
    max_sungen_version: str


class MarketplaceConfig(BaseConfig):
    """Represents marketplace-specific metadata for the plugin."""
    featured: bool
    category: str
    keywords: List[str]


class SupportConfig(BaseConfig):
    """Provides support information for the plugin."""
    documentation_url: str
    issues_url: str
    contact_email: str


class AdvancedOptionsConfig(BaseConfig):
    """Defines advanced options for the plugin's behavior."""
    parallel_install: bool
    secure_downloads: bool
    sandbox_mode: bool


class PluginSettings(BaseConfig):
    """Represents the main configuration structure for a plugin."""
    name: str
    short_name: str
    version: str
    description: str
    author: str
    source: str
    license: str
    tags: List[str]
    settings: dict
    dependencies: List[DependencyConfig]
    compatibility: CompatibilityConfig
    marketplace: MarketplaceConfig
    support: SupportConfig
    advanced: AdvancedOptionsConfig


def load_plugins(app: typer.Typer, plugin_dir: Optional[Path] = None):
    """
    Dynamically loads plugins from the specified directory based on the
    pattern "{dir_name}_plugin.py" and registers them with the main app.

    Args:
        app (typer.Typer): The main Typer app to register plugins with.
        plugin_dir (Optional[Path]): The directory to scan for plugins. Defaults to 'plugins/' relative to this file.
    """
    # Get the current module name
    current_module = __package__

    # Set default plugin directory relative to this file if none specified
    if plugin_dir is None:
        plugin_dir = Path(__file__).parent.parent / 'plugins'

    # Check if the plugin directory exists and is a directory
    if not plugin_dir.exists() or not plugin_dir.is_dir():
        raise ValueError(f"The plugin directory '{plugin_dir}' does not exist or is not a directory.")

    # Iterate over all subdirectories within the plugin directory
    for sub_dir in plugin_dir.iterdir():
        if sub_dir.is_dir():
            # Define the expected plugin filename pattern
            plugin_filename = f"{sub_dir.name}_plugin.py"
            plugin_file = sub_dir / plugin_filename

            # Check if the expected plugin file exists
            if plugin_file.exists():
                try:
                    # Construct the full module name dynamically
                    module_name = f"{current_module.rsplit('.', 1)[0]}.plugins.{sub_dir.name}.{sub_dir.name}_plugin"
                    spec = importlib.util.spec_from_file_location(module_name, plugin_file)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)

                    # Check if the module has a 'register_plugin' function
                    if hasattr(module, "register_plugin"):
                        module.register_plugin(app)  # Call the plugin's registration function

                except Exception as e:
                    print(f"Failed to load plugin '{plugin_filename}': {e}")


def create_plugin_yaml(plugin_config: PluginSettings, file_path: str = "src/sungen/plugins/marketplace/plugin.yaml"):
    """
    Create a YAML file for the plugin configuration.

    Args:
        plugin_config (PluginSettings): Plugin settings object.
        file_path (str): Path where the YAML file will be created.
    """
    # Convert the plugin configuration to a dictionary
    config_dict = plugin_config.model_dump()

    # Create directories if they do not exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the configuration to the YAML file
    with open(file_path, "w") as yaml_file:
        yaml.dump(config_dict, yaml_file, default_flow_style=False)
    print(f"Plugin configuration has been created at {file_path}")


def load_plugin_config(file_path: str = "src/sungen/plugins/marketplace/plugin.yaml") -> PluginSettings:
    """
    Load the plugin configuration from a YAML file.

    Args:
        file_path (str): Path to the YAML file containing plugin configuration.

    Returns:
        PluginSettings: Loaded plugin settings object.
    """
    return PluginSettings(config_sources=FileSource(file=file_path))


def get_plugin_metadata(plugin_config: PluginSettings):
    """
    Retrieve metadata information of a plugin.

    Args:
        plugin_config (PluginSettings): Plugin settings object.

    Returns:
        dict: Plugin metadata.
    """
    return {
        "name": plugin_config.name,
        "short_name": plugin_config.short_name,
        "version": plugin_config.version,
        "description": plugin_config.description,
        "author": plugin_config.author,
        "license": plugin_config.license
    }


def update_plugin_settings(plugin_config: PluginSettings, updates: dict):
    """
    Update the plugin settings with new values.

    Args:
        plugin_config (PluginSettings): Existing plugin settings object.
        updates (dict): Dictionary with updated settings.
    """
    # Create a new dictionary with the current config
    updated_config = plugin_config.model_dump()

    # Update the dictionary with new values
    for key, value in updates.items():
        if key in updated_config:
            if key == 'settings':
                updated_config[key].update(value)
            else:
                updated_config[key] = value

    # Create a new PluginSettings instance with the updated values
    new_plugin_config = PluginSettings(**updated_config)

    # Create the YAML file with the new configuration
    create_plugin_yaml(new_plugin_config)
    print(f"Plugin settings have been updated and saved.")

    return new_plugin_config


def validate_plugin_compatibility(plugin_config: PluginSettings, current_version: str) -> bool:
    """
    Validate the compatibility of the plugin with the current Sungen version.

    Args:
        plugin_config (PluginSettings): Plugin settings object.
        current_version (str): Current version of Sungen.

    Returns:
        bool: True if compatible, False otherwise.
    """
    min_version = plugin_config.compatibility.min_sungen_version
    max_version = plugin_config.compatibility.max_sungen_version
    return min_version <= current_version <= max_version




# Example usage
if __name__ == "__main__":
    # Example configuration for the marketplace plugin
    plugin_config = PluginSettings(
        name="Marketplace Plugin",
        short_name="mrkt",
        version="1.0.0",
        description="The Marketplace Plugin enables seamless integration with the Sungen marketplace.",
        author="Sungen Team",
        source="https://github.com/sungen/mrkt-plugin",
        license="MIT",
        tags=["marketplace", "plugin-management", "sungen"],
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
            DependencyConfig(plugin="core-plugin", version=">=1.0.0"),
            DependencyConfig(plugin="auth-plugin", version=">=1.0.0")
        ],
        compatibility=CompatibilityConfig(
            min_sungen_version="1.0.0",
            max_sungen_version="2.0.0"
        ),
        marketplace=MarketplaceConfig(
            featured=True,
            category="Utilities",
            keywords=["plugin", "marketplace", "utilities"]
        ),
        support=SupportConfig(
            documentation_url="https://docs.sungen.com/mrkt-plugin",
            issues_url="https://github.com/sungen/mrkt-plugin/issues",
            contact_email="support@sungen.com"
        ),
        advanced=AdvancedOptionsConfig(
            parallel_install=True,
            secure_downloads=True,
            sandbox_mode=False
        )
    )

    # Create YAML for the plugin
    create_plugin_yaml(plugin_config)

    # Load the plugin configuration from the YAML file
    loaded_config = load_plugin_config()
    print(get_plugin_metadata(loaded_config))
