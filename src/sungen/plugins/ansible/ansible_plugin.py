import subprocess
import typer
from typing import Optional
import importlib.util
import sys

app = typer.Typer(help="Sungen Ansible Plugin for server management tasks", name="ansible")

def run_command(command: str):
    """Helper function to run shell commands and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")

def check_installation():
    """
    Check if Ansible is installed and install it if not present.
    """
    try:
        if importlib.util.find_spec("ansible") is None:
            print("Ansible is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ansible"])
            print("Ansible has been installed successfully.")
    except Exception as e:
        print(f"Error during installation check: {str(e)}")

@app.command()
def setup():
    """Initialize or set up the server with necessary tools."""
    commands = [
        "sudo apt update",
        "sudo apt install -y curl git python3-pip",
        "sudo pip3 install ansible"
    ]
    for command in commands:
        run_command(command)
    print("Server setup complete.")

@app.command()
def deploy(file: str, destination: str):
    """Deploy a script or configuration to a specific location on the server."""
    run_command(f"cp {file} {destination}")
    print(f"Deployed {file} to {destination}.")

@app.command()
def run(task: str):
    """Run a predefined task on the server."""
    tasks = {
        "restart_server": "sudo reboot",
        "check_disk_usage": "df -h",
        "update_system": "sudo apt update && sudo apt upgrade -y"
    }
    if task not in tasks:
        print(f"Task '{task}' not found.")
        return
    run_command(tasks[task])

@app.command()
def backup(path: str, destination: str):
    """Create a backup of files on the server."""
    run_command(f"tar -czvf {destination} {path}")
    print(f"Backup of {path} created at {destination}.")

@app.command()
def update(package: Optional[str] = None):
    """Update software or packages on the server."""
    command = f"sudo apt install -y {package}" if package else "sudo apt update && sudo apt upgrade -y"
    run_command(command)

@app.command()
def check(service: Optional[str] = None):
    """Check the status of a service or the server itself."""
    command = f"systemctl status {service}" if service else "uptime"
    run_command(command)

@app.command()
def sync(local_path: str, remote_path: str):
    """Synchronize files within the server."""
    run_command(f"rsync -avz {local_path} {remote_path}")
    print(f"Synchronized {local_path} to {remote_path}.")

def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
    try:
        check_installation()
        parent_app.add_typer(app, name="ansible")
    except Exception as e:
        print(f"Failed to register plugin '{app}': {str(e)}")

if __name__ == "__main__":
    app()
