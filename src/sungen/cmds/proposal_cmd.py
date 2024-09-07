"""proposal"""
import typer


app = typer.Typer()


@app.command(name="create")
def _create():
    """create"""
    typer.echo("Running create subcommand.")
    