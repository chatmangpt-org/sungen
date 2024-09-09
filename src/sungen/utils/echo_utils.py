from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def echo(message: str, style: str = "default", panel: bool = False, title: str = None):
    """
    Custom echo function with rich formatting.
    
    Args:
    message (str): The message to be printed.
    style (str): The style to apply to the message (e.g., "bold", "italic", "green").
    panel (bool): Whether to wrap the message in a panel.
    title (str): The title of the panel (only used if panel is True).
    """
    if panel:
        console.print(Panel(Text(message, style=style), title=title))
    else:
        console.print(Text(message, style=style))