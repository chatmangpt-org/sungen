"""deploy"""
import typer


app = typer.Typer()

     
@app.command(name="deploy")
def deploy_deploy():
    """deploy"""
    typer.echo("Running deploy subcommand.")
 
@app.command(name="rollback")
def deploy_rollback():
    """rollback"""
    typer.echo("Running rollback subcommand.")
 
@app.command(name="status")
def deploy_status():
    """status"""
    typer.echo("Running status subcommand.")
 
@app.command(name="simulate")
def deploy_simulate():
    """simulate"""
    typer.echo("Running simulate subcommand.")
 
@app.command(name="deploy")
def deploy_deploy():
    """deploy"""
    typer.echo("Running deploy subcommand.")
 
@app.command(name="rollback")
def deploy_rollback():
    """rollback"""
    typer.echo("Running rollback subcommand.")
 
@app.command(name="status")
def deploy_status():
    """status"""
    typer.echo("Running status subcommand.")
 
@app.command(name="simulate")
def deploy_simulate():
    """simulate"""
    typer.echo("Running simulate subcommand.")
