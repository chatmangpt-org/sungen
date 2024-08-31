"""project"""
import typer


app = typer.Typer()


@app.command(name="project")
def _project():
    """project"""
    typer.echo("Running project subcommand.")
     
@app.command(name="init")
def project_init():
    """init"""
    typer.echo("Running init subcommand.")
 
@app.command(name="config")
def project_config():
    """config"""
    typer.echo("Running config subcommand.")
 
@app.command(name="rollback")
def project_rollback():
    """rollback"""
    typer.echo("Running rollback subcommand.")
 
@app.command(name="status")
def project_status():
    """status"""
    typer.echo("Running status subcommand.")
