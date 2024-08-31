"""inhabitant"""
import typer


app = typer.Typer()


@app.command(name="inhabitant")
def _inhabitant():
    """inhabitant"""
    typer.echo("Running inhabitant subcommand.")
     
@app.command(name="add")
def inhabitant_add():
    """add"""
    typer.echo("Running add subcommand.")
 
@app.command(name="remove")
def inhabitant_remove():
    """remove"""
    typer.echo("Running remove subcommand.")
 
@app.command(name="list")
def inhabitant_list():
    """list"""
    typer.echo("Running list subcommand.")
 
@app.command(name="start")
def inhabitant_start():
    """start"""
    typer.echo("Running start subcommand.")
 
@app.command(name="stop")
def inhabitant_stop():
    """stop"""
    typer.echo("Running stop subcommand.")
 
@app.command(name="logs")
def inhabitant_logs():
    """logs"""
    typer.echo("Running logs subcommand.")
