"""api"""
import typer


app = typer.Typer()


@app.command(name="api")
def _api():
    """api"""
    typer.echo("Running api subcommand.")
     
@app.command(name="export-openapi")
def api_export_openapi():
    """export-openapi"""
    typer.echo("Running export_openapi subcommand.")
 
@app.command(name="generate-typer")
def api_generate_typer():
    """generate-typer"""
    typer.echo("Running generate_typer subcommand.")
 
@app.command(name="docs")
def api_docs():
    """docs"""
    typer.echo("Running docs subcommand.")
 
@app.command(name="validate")
def api_validate():
    """validate"""
    typer.echo("Running validate subcommand.")
