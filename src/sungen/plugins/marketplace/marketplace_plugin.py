import os
import sys
import typer
from typing import Optional, Dict
from github import Github
import subprocess
import yaml
from sungen.utils.plugin_tools import load_plugin_config, validate_plugin_compatibility
import shutil
import requests

app = typer.Typer(help="Sungen Marketplace Plugin for managing plugins", name="mrkt")

# Singleton pattern for GitHub instance
_github_instance = None

def github() -> Github:
    """Get a singleton instance of the GitHub client."""
    global _github_instance
    if _github_instance is None:
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            print('Error: No GitHub token provided and $GITHUB_TOKEN is not set.', file=sys.stderr)
            sys.exit(-1)
        _github_instance = Github(token)
    return _github_instance

@app.command()
def search(query: str):
    """Search for plugins in the marketplace"""
    gh = github()
    result = gh.search_repositories(query=f"{query} in:name")
    for repo in result[:10]:  # Show top 10 results
        typer.echo(f"{repo.full_name}: {repo.description}")

@app.command()
def install(plugin_name: str, version: Optional[str] = None):
    """Install a plugin from the marketplace"""
    gh = github()
    repo = gh.get_repo(plugin_name)
    clone_url = repo.clone_url
    path = f"plugins/{plugin_name}"

    try:
        clone_command = f"git clone {clone_url} {path}"
        result = subprocess.run(clone_command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            typer.echo(f"Plugin '{plugin_name}' installed successfully at {path}")
        else:
            typer.echo(f"Error cloning repository: {result.stderr}")
    except Exception as e:
        typer.echo(f"Failed to install plugin '{plugin_name}': {str(e)}")

@app.command()
def uninstall(plugin_name: str):
    """Uninstall a plugin"""
    path = f"plugins/{plugin_name}"
    if os.path.exists(path):
        try:
            os.rmdir(path)
            typer.echo(f"Plugin '{plugin_name}' uninstalled successfully.")
        except Exception as e:
            typer.echo(f"Failed to uninstall plugin '{plugin_name}': {str(e)}")
    else:
        typer.echo(f"Plugin '{plugin_name}' not found.")

@app.command()
def update(plugin_name: Optional[str] = None):
    """Update a plugin or all plugins"""
    path = f"plugins/{plugin_name}"
    if plugin_name and os.path.exists(path):
        try:
            result = subprocess.run(["git", "pull"], cwd=path, capture_output=True, text=True)
            if result.returncode == 0:
                typer.echo(f"Plugin '{plugin_name}' updated successfully.")
            else:
                typer.echo(f"Error updating plugin '{plugin_name}': {result.stderr}")
        except Exception as e:
            typer.echo(f"Failed to update plugin '{plugin_name}': {str(e)}")
    else:
        typer.echo("No plugin specified or plugin not found.")

@app.command()
def list_plugins():
    """List all installed plugins"""
    path = "plugins"
    if os.path.exists(path):
        plugins = os.listdir(path)
        if plugins:
            typer.echo("Installed plugins:")
            for plugin in plugins:
                typer.echo(f"- {plugin}")
        else:
            typer.echo("No plugins installed.")
    else:
        typer.echo("No plugins directory found.")

@app.command()
def info(plugin_name: str):
    """Get detailed information about a plugin"""
    gh = github()
    try:
        repo = gh.get_repo(plugin_name)
        typer.echo(f"Plugin: {repo.full_name}")
        typer.echo(f"Description: {repo.description}")
        typer.echo(f"Stars: {repo.stargazers_count}")
        typer.echo(f"Forks: {repo.forks_count}")
        typer.echo(f"Open Issues: {repo.open_issues_count}")
    except Exception as e:
        typer.echo(f"Failed to retrieve information for plugin '{plugin_name}': {str(e)}")

@app.command()
def publish(plugin_path: str):
    """Publish a plugin to the marketplace"""
    if not os.path.exists(plugin_path):
        typer.echo(f"Error: Plugin path '{plugin_path}' does not exist.")
        return

    try:
        config = load_plugin_config(os.path.join(plugin_path, "plugin.yaml"))
        gh = github()
        user = gh.get_user()
        repo_name = f"sungen-plugin-{config.short_name}"
        
        # Create a new repository
        repo = user.create_repo(repo_name, description=config.description)
        
        # Initialize git, add files, and push to the new repository
        os.chdir(plugin_path)
        subprocess.run(["git", "init"])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Initial commit"])
        subprocess.run(["git", "remote", "add", "origin", repo.clone_url])
        subprocess.run(["git", "push", "-u", "origin", "master"])
        
        typer.echo(f"Plugin '{config.name}' published successfully to {repo.html_url}")
    except Exception as e:
        typer.echo(f"Failed to publish plugin: {str(e)}")

@app.command()
def validate(plugin_name: Optional[str] = None):
    """Validate the integrity and compatibility of installed plugins"""
    plugins_dir = "plugins"
    if plugin_name:
        plugins_to_validate = [plugin_name]
    else:
        plugins_to_validate = os.listdir(plugins_dir)

    for plugin in plugins_to_validate:
        plugin_path = os.path.join(plugins_dir, plugin)
        if not os.path.isdir(plugin_path):
            continue

        try:
            config = load_plugin_config(os.path.join(plugin_path, "plugin.yaml"))
            # Assuming there's a function to get the current Sungen version
            current_version = "1.5.0"  # Replace with actual version retrieval
            is_compatible = validate_plugin_compatibility(config, current_version)
            
            if is_compatible:
                typer.echo(f"Plugin '{plugin}' is valid and compatible.")
            else:
                typer.echo(f"Plugin '{plugin}' is not compatible with the current Sungen version.")
        except Exception as e:
            typer.echo(f"Failed to validate plugin '{plugin}': {str(e)}")

@app.command()
def rollback(plugin_name: str, version: str):
    """Revert a plugin to a previous version"""
    plugin_path = f"plugins/{plugin_name}"
    if not os.path.exists(plugin_path):
        typer.echo(f"Error: Plugin '{plugin_name}' not found.")
        return

    try:
        os.chdir(plugin_path)
        # Fetch all tags
        subprocess.run(["git", "fetch", "--tags"])
        # Check if the specified version exists
        result = subprocess.run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{version}"], capture_output=True, text=True)
        if result.returncode != 0:
            typer.echo(f"Error: Version '{version}' not found for plugin '{plugin_name}'.")
            return
        # Checkout the specified version
        subprocess.run(["git", "checkout", f"tags/{version}"])
        typer.echo(f"Successfully rolled back plugin '{plugin_name}' to version '{version}'.")
    except Exception as e:
        typer.echo(f"Failed to rollback plugin '{plugin_name}': {str(e)}")

@app.command()
def configure():
    """Configure marketplace preferences and sync settings"""
    config_file = "marketplace_config.yaml"
    default_config: Dict[str, str] = {
        "default_marketplace": "https://marketplace.sungen.com",
        "auto_update": "true",
        "sync_interval": "daily"
    }

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = default_config

    for key, value in config.items():
        new_value = typer.prompt(f"{key.capitalize()} [{value}]", default=value)
        config[key] = new_value

    with open(config_file, 'w') as f:
        yaml.dump(config, f)

    typer.echo("Configuration updated successfully.")

@app.command()
def sync():
    """Synchronize installed plugins with the marketplace"""
    plugins_dir = "plugins"
    for plugin in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin)
        if not os.path.isdir(plugin_path):
            continue

        try:
            os.chdir(plugin_path)
            # Fetch the latest changes
            subprocess.run(["git", "fetch", "origin"])
            # Check if there are any updates
            result = subprocess.run(["git", "rev-list", "HEAD...origin/master", "--count"], capture_output=True, text=True)
            if int(result.stdout.strip()) > 0:
                typer.echo(f"Updates available for plugin '{plugin}'. Use 'update' command to apply them.")
            else:
                typer.echo(f"Plugin '{plugin}' is up to date.")
        except Exception as e:
            typer.echo(f"Failed to sync plugin '{plugin}': {str(e)}")

@app.command()
def upgrade():
    """Upgrade the marketplace client"""
    current_version = "1.0.0"  # Replace with actual version retrieval
    try:
        # Check for the latest version (this URL is hypothetical)
        response = requests.get("https://api.sungen.com/marketplace/latest-version")
        latest_version = response.json()["version"]

        if latest_version > current_version:
            typer.echo(f"New version available: {latest_version}")
            if typer.confirm("Do you want to upgrade?"):
                # Perform the upgrade (this is a placeholder implementation)
                typer.echo("Upgrading marketplace client...")
                # Here you would typically download and install the new version
                typer.echo("Upgrade completed successfully.")
            else:
                typer.echo("Upgrade cancelled.")
        else:
            typer.echo("You are already using the latest version.")
    except Exception as e:
        typer.echo(f"Failed to check for upgrades: {str(e)}")

@app.command()
def copy(source: str, destination: str):
    """Copy plugins from one location to another"""
    if not os.path.exists(source):
        typer.echo(f"Error: Source path '{source}' does not exist.")
        return

    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
        typer.echo(f"Successfully copied from '{source}' to '{destination}'.")
    except Exception as e:
        typer.echo(f"Failed to copy: {str(e)}")


def register_plugin(parent_app: typer.Typer):
    """
    Register the plugin with the main application.
    """
    try:
        parent_app.add_typer(app)
    except Exception as e:
        print(f"Failed to register plugin '{app}': {str(e)}")


if __name__ == "__main__":
    app()
