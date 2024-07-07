"""sungen CLI."""
from pathlib import Path

import typer
from rich import print

from sungen.utils.cli_tools import load_commands
from sungen.utils.file_tools import source_dir

app = typer.Typer()


load_commands(app, source_dir("cmds"))


@app.command()
def fire(name: str = "Chell") -> None:
    """Fire portal gun."""
    print(f"[bold red]Alert![/bold red] {name} fired [green]portal gun[/green] :boom:")


def main():
    """Main function"""


if __name__ == '__main__':
    main()
