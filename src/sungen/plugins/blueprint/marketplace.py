# blueprint_marketplace.py

import os
import typer
import requests
from pydantic import BaseModel as PydanticBaseModel
from typing import List
import yaml

# Typer app for managing the blueprint marketplace
marketplace_app = typer.Typer(
    name="marketplace",
    help="Marketplace for downloading, uploading, and managing blueprints."
)

MARKETPLACE_URL = "https://api.github.com/repos/your-org/blueprint-marketplace/contents"  # Replace with actual URL

class BlueprintInfo(PydanticBaseModel):
    """Model to represent blueprint metadata."""
    name: str
    description: str
    version: str
    author: str
    rating: float
    download_url: str

@marketplace_app.command()
def browse_blueprints():
    """
    List all available blueprints in the marketplace.
    """
    try:
        response = requests.get(MARKETPLACE_URL)
        response.raise_for_status()

        blueprints = response.json()
        if not blueprints:
            typer.echo("No blueprints found in the marketplace.")
            return

        typer.echo("Available blueprints in the marketplace:")
        for blueprint in blueprints:
            blueprint_info = BlueprintInfo(**blueprint)
            typer.echo(f"- {blueprint_info.name} (v{blueprint_info.version}) by {blueprint_info.author} - Rating: {blueprint_info.rating} stars")
            typer.echo(f"  Description: {blueprint_info.description}")

    except requests.RequestException as e:
        typer.echo(f"Error fetching blueprints from the marketplace: {e}")
        raise typer.Exit(code=1)


@marketplace_app.command()
def download_blueprint(name: str):
    """
    Download a specific blueprint by name from the marketplace.
    """
    try:
        response = requests.get(f"{MARKETPLACE_URL}/{name}.yml")
        response.raise_for_status()

        with open(f"{name}.yml", "wb") as blueprint_file:
            blueprint_file.write(response.content)

        typer.echo(f"Blueprint '{name}' downloaded successfully.")

    except requests.RequestException as e:
        typer.echo(f"Error downloading blueprint '{name}': {e}")
        raise typer.Exit(code=1)


@marketplace_app.command()
def upload_blueprint(file_path: str, author: str):
    """
    Upload a blueprint to the marketplace.
    """
    if not os.path.exists(file_path):
        typer.echo(f"File '{file_path}' not found.")
        raise typer.Exit(code=1)

    try:
        with open(file_path, "r") as file:
            content = file.read()

        blueprint_name = os.path.basename(file_path)

        # Placeholder code for uploading to GitHub repository
        # You would need a GitHub token and proper permissions for uploading
        response = requests.put(
            f"{MARKETPLACE_URL}/{blueprint_name}",
            headers={"Authorization": "token YOUR_GITHUB_TOKEN"},
            json={"content": content, "message": f"Upload {blueprint_name} by {author}"}
        )

        response.raise_for_status()
        typer.echo(f"Blueprint '{file_path}' uploaded successfully to the marketplace.")

    except requests.RequestException as e:
        typer.echo(f"Error uploading blueprint '{file_path}': {e}")
        raise typer.Exit(code=1)


@marketplace_app.command()
def search_blueprints(keyword: str):
    """
    Search for blueprints in the marketplace by keyword.
    """
    try:
        response = requests.get(MARKETPLACE_URL)
        response.raise_for_status()

        blueprints = response.json()
        if not blueprints:
            typer.echo("No blueprints found in the marketplace.")
            return

        filtered_blueprints = [bp for bp in blueprints if keyword.lower() in bp['name'].lower() or keyword.lower() in bp['description'].lower()]

        if not filtered_blueprints:
            typer.echo(f"No blueprints found matching keyword '{keyword}'.")
            return

        typer.echo(f"Blueprints matching '{keyword}':")
        for blueprint in filtered_blueprints:
            blueprint_info = BlueprintInfo(**blueprint)
            typer.echo(f"- {blueprint_info.name} (v{blueprint_info.version}) by {blueprint_info.author} - Rating: {blueprint_info.rating} stars")
            typer.echo(f"  Description: {blueprint_info.description}")

    except requests.RequestException as e:
        typer.echo(f"Error searching blueprints in the marketplace: {e}")
        raise typer.Exit(code=1)


@marketplace_app.command()
def rate_blueprint(name: str, rating: float):
    """
    Rate a blueprint in the marketplace.
    """
    if rating < 0 or rating > 5:
        typer.echo("Rating must be between 0 and 5.")
        raise typer.Exit(code=1)

    try:
        response = requests.patch(
            f"{MARKETPLACE_URL}/{name}",
            headers={"Authorization": "token YOUR_GITHUB_TOKEN"},
            json={"rating": rating}
        )
        response.raise_for_status()
        typer.echo(f"Blueprint '{name}' rated with {rating} stars successfully.")

    except requests.RequestException as e:
        typer.echo(f"Error rating blueprint '{name}': {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    marketplace_app()
