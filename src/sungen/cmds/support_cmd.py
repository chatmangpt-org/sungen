"""support"""
import typer


app = typer.Typer()


@app.command(name="support")
def _support():
    """support"""
    typer.echo("Running support subcommand.")
     
@app.command(name="help")
def support_help():
    """help"""
    typer.echo("Running help subcommand.")
 
@app.command(name="docs")
def support_docs():
    """docs"""
    typer.echo("Running docs subcommand.")
 
@app.command(name="contact")
def support_contact():
    """contact"""
    typer.echo("Running contact subcommand.")
 
@app.command(name="version")
def support_version():
    """version"""
    typer.echo("Running version subcommand.")
 
@app.command(name="feedback")
def support_feedback():
    """feedback"""
    typer.echo("Running feedback subcommand.")
