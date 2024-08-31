import typer

from sungen.utils.git_tools import github

# Create a Typer app for the branch commands
app = typer.Typer()

# Command to create a new branch
@app.command("create")
def create_branch(
    repo_name: str = typer.Option(..., "-r", "--repo", help="Name of the repository"),
    branch_name: str = typer.Option(..., "-b", "--branch", help="Name of the new branch"),
    base_branch: str = typer.Option("main", "-B", "--base", help="Base branch to create the new branch from"),
):
    repo = github().get_user().get_repo(repo_name)
    base_ref = repo.get_git_ref(f"heads/{base_branch}")
    new_ref = repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_ref.object.sha)

    typer.echo(f"Created new branch '{branch_name}' from '{base_branch}' in repository '{repo_name}'.")

# Command to delete a branch
@app.command("delete")
def delete_branch(
    repo_name: str = typer.Option(..., "-r", "--repo", help="Name of the repository"),
    branch_name: str = typer.Option(..., "-b", "--branch", help="Name of the branch to delete"),
):
    repo = github().get_user().get_repo(repo_name)
    ref = repo.get_git_ref(f"heads/{branch_name}")
    ref.delete()

    typer.echo(f"Deleted branch '{branch_name}' from repository '{repo_name}'.")

# Command to list all branches in a repository
@app.command("list")
def list_branches(
    repo_name: str = typer.Option(..., "-r", "--repo", help="Name of the repository"),
):
    repo = github().get_user().get_repo(repo_name)
    branches = repo.get_branches()

    typer.echo(f"Branches in repository '{repo_name}':")
    for branch in branches:
        typer.echo(f"- {branch.name}")

@app.command("merge")
def merge_branch(
    repo_name: str = typer.Option(..., "-r", "--repo", help="Name of the repository"),
    head: str = typer.Option(..., "--head", help="The name of the branch to merge from"),
    base: str = typer.Option(..., "--base", help="The name of the branch to merge into"),
    commit_message: str = typer.Option(None, "--message", "-m", help="Commit message for the merge")
):
    """Merge one branch into another."""
    repo = github().get_user().get_repo(repo_name)
    merge_result = repo.merge(base, head, commit_message)
    typer.echo(f"Merged '{head}' into '{base}'. Commit SHA: {merge_result.sha}")

@app.command("protect")
def protect_branch(
    repo_name: str = typer.Option(..., "-r", "--repo", help="Name of the repository"),
    branch_name: str = typer.Option(..., "-b", "--branch", help="Name of the branch to protect"),
    require_pr: bool = typer.Option(True, help="Require pull request reviews before merging"),
    required_approvals: int = typer.Option(1, help="Number of required approving reviews")
):
    """Set branch protection rules."""
    repo = github().get_user().get_repo(repo_name)
    branch = repo.get_branch(branch_name)
    branch.edit_protection(required_approving_review_count=required_approvals, require_pull_request_reviews=require_pr)
    typer.echo(f"Protection rules set for branch '{branch_name}' in repository '{repo_name}'.")

@app.command("rename")
def rename_branch(
    repo_name: str = typer.Option(..., "-r", "--repo", help="Name of the repository"),
    old_name: str = typer.Option(..., "--old", help="Current name of the branch"),
    new_name: str = typer.Option(..., "--new", help="New name for the branch")
):
    """Rename a branch."""
    repo = github().get_user().get_repo(repo_name)
    git_ref = repo.get_git_ref(f"heads/{old_name}")
    git_ref.edit(ref=f"refs/heads/{new_name}")
    repo.get_git_ref(f"heads/{old_name}").delete()
    typer.echo(f"Branch '{old_name}' renamed to '{new_name}' in repository '{repo_name}'.")

@app.command("compare")
def compare_branches(
    repo_name: str = typer.Option(..., "-r", "--repo", help="Name of the repository"),
    base: str = typer.Option(..., "--base", help="Base branch for comparison"),
    head: str = typer.Option(..., "--head", help="Head branch for comparison")
):
    """Compare two branches."""
    repo = github().get_user().get_repo(repo_name)
    comparison = repo.compare(base, head)
    typer.echo(f"Comparing {base}...{head} in repository '{repo_name}':")
    typer.echo(f"Commits ahead: {comparison.ahead_by}")
    typer.echo(f"Commits behind: {comparison.behind_by}")
    typer.echo(f"Diff URL: {comparison.html_url}")

@app.command("set-default")
def set_default_branch(
    repo_name: str = typer.Option(..., "-r", "--repo", help="Name of the repository"),
    branch_name: str = typer.Option(..., "-b", "--branch", help="Name of the branch to set as default")
):
    """Set the default branch for a repository."""
    repo = github().get_user().get_repo(repo_name)
    repo.edit(default_branch=branch_name)
    typer.echo(f"Default branch for repository '{repo_name}' set to '{branch_name}'.")

"""
mix archive.install hex phx_new

mix igniter.new helpdesk \
  --install ash,ash_postgres \
  --with phx.new \
  --extend postgres \
  --example
"""