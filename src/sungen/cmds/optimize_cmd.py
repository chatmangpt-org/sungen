"""optimize"""
import typer


app = typer.Typer()


@app.command(name="optimize")
def _optimize():
    """optimize"""
    typer.echo("Running optimize subcommand.")
     
@app.command(name="apply-triz")
def optimize_apply_triz():
    """apply-triz"""
    typer.echo("Running apply_triz subcommand.")
 
@app.command(name="performance")
def optimize_performance():
    """performance"""
    typer.echo("Running performance subcommand.")
 
@app.command(name="resource-usage")
def optimize_resource_usage():
    """resource-usage"""
    typer.echo("Running resource_usage subcommand.")
 
@app.command(name="security")
def optimize_security():
    """security"""
    typer.echo("Running security subcommand.")
