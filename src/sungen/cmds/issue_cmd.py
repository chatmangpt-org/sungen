"""issue"""
import typer
from sungen.utils.git_tools import github

app = typer.Typer()

@app.command(name="create")
def issue_create(
    title: str = typer.Option(..., "--title", "-t", help="Title of the issue"),
    body: str = typer.Option("", "--body", "-b", help="Body of the issue"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Create a new issue in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    issue = repo_obj.create_issue(title=title, body=body)
    typer.echo(f"Created issue #{issue.number}: {issue.title}")
    typer.echo(f"URL: {issue.html_url}")

@app.command(name="close")
def issue_close(
    number: int = typer.Option(..., "--number", "-n", help="Issue number to close"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Close an existing issue in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    issue = repo_obj.get_issue(number=number)
    issue.edit(state="closed")
    typer.echo(f"Closed issue #{issue.number}: {issue.title}")

@app.command(name="list")
def issue_list(
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)"),
    state: str = typer.Option("open", "--state", "-s", help="State of issues to list (open, closed, all)")
):
    """List issues in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    issues = repo_obj.get_issues(state=state)

    typer.echo(f"Issues in {repo} ({state}):")
    for issue in issues:
        typer.echo(f"#{issue.number}: {issue.title} - {issue.state}")

@app.command(name="comment")
def issue_comment(
    number: int = typer.Option(..., "--number", "-n", help="Issue number to comment on"),
    body: str = typer.Option(..., "--body", "-b", help="Comment body"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Add a comment to an existing issue in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    issue = repo_obj.get_issue(number=number)
    comment = issue.create_comment(body)
    typer.echo(f"Added comment to issue #{issue.number}")
    typer.echo(f"Comment URL: {comment.html_url}")

@app.command(name="update")
def issue_update(
    number: int = typer.Option(..., "--number", "-n", help="Issue number to update"),
    title: str = typer.Option(None, "--title", "-t", help="New title for the issue"),
    body: str = typer.Option(None, "--body", "-b", help="New body for the issue"),
    state: str = typer.Option(None, "--state", "-s", help="New state for the issue (open or closed)"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Update an existing issue in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    issue = repo_obj.get_issue(number=number)
    
    update_params = {}
    if title:
        update_params["title"] = title
    if body:
        update_params["body"] = body
    if state:
        update_params["state"] = state
    
    issue.edit(**update_params)
    typer.echo(f"Updated issue #{issue.number}: {issue.title}")
    typer.echo(f"URL: {issue.html_url}")

@app.command(name="assign")
def issue_assign(
    number: int = typer.Option(..., "--number", "-n", help="Issue number to assign"),
    assignee: str = typer.Option(..., "--assignee", "-a", help="GitHub username to assign the issue to"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Assign an issue to a GitHub user."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    issue = repo_obj.get_issue(number=number)
    issue.add_to_assignees(assignee)
    typer.echo(f"Assigned issue #{issue.number} to {assignee}")

@app.command(name="labels")
def issue_labels(
    number: int = typer.Option(..., "--number", "-n", help="Issue number to modify labels"),
    add: list[str] = typer.Option([], "--add", help="Labels to add to the issue"),
    remove: list[str] = typer.Option([], "--remove", help="Labels to remove from the issue"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Add or remove labels from an issue."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    issue = repo_obj.get_issue(number=number)
    
    if add:
        issue.add_to_labels(*add)
    if remove:
        issue.remove_from_labels(*remove)

    typer.echo(f"Updated labels for issue #{issue.number}")

    issue = repo_obj.get_issue(number=number)
    
    typer.echo(f"Current labels: {', '.join([label.name for label in issue.labels])}")
    