from pathlib import Path
from sungen.utils.cli_tools import load_commands

# ... other imports and code ...

load_commands(app, Path("src/ash/cmds"))