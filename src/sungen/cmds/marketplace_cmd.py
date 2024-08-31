"""marketplace"""
import typer


app = typer.Typer()


@app.command(name="marketplace")
def marketplace_marketplace():
    """marketplace"""
    typer.echo("Running marketplace subcommand.")
     
@app.command(name="list")
def marketplace_list():
    """list"""
    typer.echo("Running list subcommand.")
 
@app.command(name="install")
def marketplace_install():
    """install"""
    typer.echo("Running install subcommand.")
 
@app.command(name="uninstall")
def marketplace_uninstall():
    """uninstall"""
    typer.echo("Running uninstall subcommand.")
 
@app.command(name="update")
def marketplace_update():
    """update"""
    typer.echo("Running update subcommand.")
 
@app.command(name="search")
def marketplace_search():
    """search"""
    typer.echo("Running search subcommand.")
