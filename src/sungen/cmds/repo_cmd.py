"""repo"""
import typer
import os
import subprocess

from sungen.utils.cli_tools import load_commands
from sungen.utils.file_tools import source_dir
from sungen.utils.git_tools import github

app = typer.Typer()

def first_commit(
    name: str,
    commit_message: str = "Initial commit",
    branch: str = "main",
    path: str = "."
):
    """
    Create an initial commit in the specified repository.
    """
    gh = github()
    user = gh.get_user()
    repo = user.get_repo(name)

    # Change to the specified path
    os.chdir(path)

    # Clone the repository
    subprocess.run(["git", "clone", repo.clone_url, name], check=True)
    os.chdir(os.path.join(path, name))  # Change directory to the cloned repo

    # Create a README.md
    with open("README.md", "w") as f:
        f.write(f"# {name}\n\nThis is the {name} repository.")

    # Stage, commit, and push the changes
    subprocess.run(["git", "add", "README.md"], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "branch", "-M", branch], check=True)
    subprocess.run(["git", "push", "-u", "origin", branch], check=True)

    return f"First commit created and pushed to branch '{branch}' in repository '{name}' at {repo.html_url}"

@app.command("first-commit")
def first_commit_(
    name: str = typer.Argument(..., help="Name of the repository"),
    commit_message: str = typer.Option("Initial commit", "--message", "-m", help="Commit message"),
    branch: str = typer.Option("main", "--branch", "-b", help="Branch name"),
    path: str = typer.Option(".", "--path", "-p", help="Path to the repository")
):
    """
    Create an initial commit in the specified repository.
    """
    result = first_commit(name, commit_message, branch, path)
    typer.echo(result)

@app.command("create")
def create_(
    name: str = typer.Option(..., "-n", "--name", help="Name of the new repository"),
    description: str = typer.Option("", "-d", "--description", help="Description of the repository"),
    private: bool = typer.Option(True, "-p", "--private", help="Set the repository to private"),
    first: bool = typer.Option(False, "--first-commit", "-f", help="Create an initial commit after creating the repository")
):
    """
    Create a new GitHub repository with a description.
    """
    gh = github()
    user = gh.get_user()
    repo = user.create_repo(name=name, description=description, private=private)
    typer.echo(f"Created repository '{repo.full_name}' at {repo.html_url}")

    # Optionally create the first commit
    if first:
        typer.echo("Creating the first commit...")
        result = first_commit(name)
        typer.echo(result)

@app.command(name="new")
def new_():
    """new"""
    typer.echo("Running new subcommand.")


@app.command(name="list")
def list_():
    """
    List all repositories for the authenticated user.
    """
    gh = github()
    user = gh.get_user()
    repos = user.get_repos()

    typer.echo("Your repositories:")
    for repo in repos:
        typer.echo(f"- {repo.full_name}")


@app.command("delete")
def delete_(
    name: str = typer.Option(..., "--name", "-n", help="Name of the repository to delete"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt")
):
    """
    Delete a GitHub repository.
    """
    gh = github()
    user = gh.get_user()
    
    if not confirm:
        typer.confirm(f"Are you sure you want to delete the repository '{name}'?", abort=True)
    
    user.get_repo(name).delete()
    typer.echo(f"Repository '{name}' has been deleted.")

@app.command("update")
def update_(
    name: str = typer.Option(..., "--name", "-n", help="Name of the repository to update"),
    new_name: str = typer.Option(None, "--new-name", help="New name for the repository"),
    description: str = typer.Option(None, "--description", "-d", help="New description for the repository"),
    private: bool = typer.Option(None, "--private", "-p", help="Set the repository to private")
):
    """
    Update a GitHub repository's properties.
    """
    gh = github()
    user = gh.get_user()
    repo = user.get_repo(name)
    
    if new_name:
        repo.edit(name=new_name)
    if description is not None:
        repo.edit(description=description)
    if private is not None:
        repo.edit(private=private)
    
    typer.echo(f"Repository '{repo.full_name}' has been updated.")

@app.command("clone")
def clone_(
    name: str = typer.Option(..., "--name", "-n", help="Name of the repository to clone"),
    path: str = typer.Option(".", "--path", "-p", help="Path to clone the repository to")
):
    """
    Clone a GitHub repository.
    """
    gh = github()
    user = gh.get_user()
    repo = user.get_repo(name)
    
    import subprocess
    
    clone_command = f"git clone {repo.clone_url} {path}"
    result = subprocess.run(clone_command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        typer.echo(f"Repository '{repo.full_name}' has been cloned to {path}")
    else:
        typer.echo(f"Error cloning repository: {result.stderr}")

@app.command("fork")
def fork_(
    name: str = typer.Option(..., "--name", "-n", help="Name of the repository to fork"),
    organization: str = typer.Option(None, "--org", "-o", help="Organization to fork the repository to")
):
    """
    Fork a GitHub repository.
    """
    gh = github()
    repo = gh.get_repo(name)
    
    if organization:
        forked_repo = repo.create_fork(organization=organization)
    else:
        forked_repo = repo.create_fork()
    
    typer.echo(f"Repository '{repo.full_name}' has been forked to '{forked_repo.full_name}'")

@app.command("add-collaborator")
def add_collaborator_(
    name: str = typer.Option(..., "--name", "-n", help="Name of the repository"),
    username: str = typer.Option(..., "--user", "-u", help="Username of the collaborator to add"),
    permission: str = typer.Option("push", "--permission", "-p", help="Permission level (pull, push, admin)")
):
    """
    Add a collaborator to a GitHub repository.
    """
    gh = github()
    user = gh.get_user()
    repo = user.get_repo(name)
    
    repo.add_to_collaborators(username, permission=permission)
    typer.echo(f"Added {username} as a collaborator to '{repo.full_name}' with {permission} permissions.")