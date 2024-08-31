"""pr"""
import typer
from sungen.utils.git_tools import github

app = typer.Typer()

@app.command(name="create")
def pr_create(
    title: str = typer.Option(..., "--title", "-t", help="Title of the pull request"),
    body: str = typer.Option("", "--body", "-b", help="Body of the pull request"),
    head: str = typer.Option(..., "--head", "-h", help="The name of the branch where your changes are implemented"),
    base: str = typer.Option("main", "--base", help="The name of the branch you want the changes pulled into"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Create a new pull request in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    pr = repo_obj.create_pull(title=title, body=body, head=head, base=base)
    typer.echo(f"Created pull request #{pr.number}: {pr.title}")
    typer.echo(f"URL: {pr.html_url}")

@app.command(name="merge")
def pr_merge(
    number: int = typer.Option(..., "--number", "-n", help="Pull request number to merge"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)"),
    merge_method: str = typer.Option("merge", "--method", "-m", help="Merge method (merge, squash, or rebase)")
):
    """Merge an existing pull request in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    pr = repo_obj.get_pull(number=number)
    pr.merge(merge_method=merge_method)
    typer.echo(f"Merged pull request #{pr.number}: {pr.title}")

@app.command(name="close")
def pr_close(
    number: int = typer.Option(..., "--number", "-n", help="Pull request number to close"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Close an existing pull request in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    pr = repo_obj.get_pull(number=number)
    pr.edit(state="closed")
    typer.echo(f"Closed pull request #{pr.number}: {pr.title}")

@app.command(name="list")
def pr_list(
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)"),
    state: str = typer.Option("open", "--state", "-s", help="State of pull requests to list (open, closed, all)")
):
    """List pull requests in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    prs = repo_obj.get_pulls(state=state)

    typer.echo(f"Pull requests in {repo} ({state}):")
    for pr in prs:
        typer.echo(f"#{pr.number}: {pr.title} - {pr.state}")

@app.command(name="comment")
def pr_comment(
    number: int = typer.Option(..., "--number", "-n", help="Pull request number to comment on"),
    body: str = typer.Option(..., "--body", "-b", help="Comment body"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Add a comment to an existing pull request in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    pr = repo_obj.get_pull(number=number)
    comment = pr.create_issue_comment(body)
    typer.echo(f"Added comment to pull request #{pr.number}")
    typer.echo(f"Comment URL: {comment.html_url}")

@app.command(name="update")
def pr_update(
    number: int = typer.Option(..., "--number", "-n", help="Pull request number to update"),
    title: str = typer.Option(None, "--title", "-t", help="New title for the pull request"),
    body: str = typer.Option(None, "--body", "-b", help="New body for the pull request"),
    state: str = typer.Option(None, "--state", "-s", help="New state for the pull request (open or closed)"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Update an existing pull request in a GitHub repository."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    pr = repo_obj.get_pull(number=number)
    
    update_params = {}
    if title:
        update_params["title"] = title
    if body:
        update_params["body"] = body
    if state:
        update_params["state"] = state
    
    pr.edit(**update_params)
    typer.echo(f"Updated pull request #{pr.number}: {pr.title}")
    typer.echo(f"URL: {pr.html_url}")

@app.command(name="assign")
def pr_assign(
    number: int = typer.Option(..., "--number", "-n", help="Pull request number to assign"),
    assignee: str = typer.Option(..., "--assignee", "-a", help="GitHub username to assign the pull request to"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Assign a pull request to a GitHub user."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    pr = repo_obj.get_pull(number=number)
    pr.add_to_assignees(assignee)
    typer.echo(f"Assigned pull request #{pr.number} to {assignee}")

@app.command(name="labels")
def pr_labels(
    number: int = typer.Option(..., "--number", "-n", help="Pull request number to modify labels"),
    add: list[str] = typer.Option([], "--add", help="Labels to add to the pull request"),
    remove: list[str] = typer.Option([], "--remove", help="Labels to remove from the pull request"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Add or remove labels from a pull request."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    pr = repo_obj.get_pull(number=number)
    
    if add:
        pr.add_to_labels(*add)
    if remove:
        pr.remove_from_labels(*remove)

    typer.echo(f"Updated labels for pull request #{pr.number}")

    pr = repo_obj.get_pull(number=number)
    
    typer.echo(f"Current labels: {', '.join([label.name for label in pr.labels])}")

@app.command(name="review")
def pr_review(
    number: int = typer.Option(..., "--number", "-n", help="Pull request number to review"),
    body: str = typer.Option(..., "--body", "-b", help="Review comment"),
    event: str = typer.Option("COMMENT", "--event", "-e", help="Review event (APPROVE, REQUEST_CHANGES, or COMMENT)"),
    repo: str = typer.Option(..., "--repo", "-r", help="Repository name (owner/repo)")
):
    """Submit a review for a pull request."""
    gh = github()
    repo_obj = gh.get_repo(repo)
    pr = repo_obj.get_pull(number=number)
    review = pr.create_review(body=body, event=event)
    typer.echo(f"Submitted {event} review for pull request #{pr.number}")
    typer.echo(f"Review URL: {review.html_url}")
    