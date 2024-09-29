from sungen.utils.chat_tools import handle_global_error, set_global_exception_handler

set_global_exception_handler()

import json
import subprocess
import sys
from importlib import metadata

import typer
from munch import Munch
from rich import print
from sungen.utils.cli_tools import load_commands, source_dir
import os

from sungen.utils.plugin_tools import load_plugins


app = typer.Typer()

# Remove safe imports and exception handling for loading commands and plugins
load_commands(app, source_dir("cmds"))
load_plugins(app)


@app.command()
def init(project_name: str = typer.Argument(...),
         author_email: str = typer.Argument("todo@todo.com"),
         author_name: str = typer.Argument("TODO")):
    """Initialize the sungen project."""
    # If the project has underscores or spaces throw an error
    if "_" in project_name or " " in project_name:
        print("Project name should not contain underscores or spaces.")
        sys.exit(1)
    elif project_name[0] == "-" or project_name[0] == "_":
        print("Project name should not start with a hyphen or underscore.")
        sys.exit(1)

    # check_or_install_packages()

    extra_context = Munch(project_name=project_name,
                          author_email=author_email,
                          author_name=author_name)

    # The template URL and the configuration for the new project
    template_url = "https://github.com/radix-ai/poetry-cookiecutter"
    # Project initialization logic, assuming static configuration for demonstration
    print(f"Creating new project named {project_name}...")
    subprocess.check_call(["cruft", "create", template_url,
                           "--config-file", source_dir("config.yaml"),
                           "--extra-context", f'{json.dumps(extra_context)}',
                           "--no-input"])

    # We need to install sungen in the project's virtual environment
    # It uses poetry to manage the virtual environment
    # Change to the project directory
    # Run the command to initialize the virtual environment
    # Run the command to install sungen in the virtual environment

    os.chdir(project_name)

    subprocess.check_call(["poetry", "install"])
    # Create the virtual environment
    subprocess.check_call(["poetry", "env", "use", "python"])
    # Install the project in the virtual environment
    subprocess.check_call(["poetry", "add", "sungen"])

    subprocess.check_call(["poetry", "run", "pip", "install", "-e", "."])
    # Change back to the original directory
    os.chdir("..")

    print(f"Project {project_name} initialized successfully.")


# def process_voice_command():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
#
#         # Loop to continuously listen and recognize speech
#         while True:
#             try:
#                 print("Listening for a command...")
#                 audio = recognizer.listen(source, phrase_time_limit=5)  # Listen for a maximum of 5 seconds per phrase
#
#                 # Recognize the audio and convert it to text
#                 command = recognizer.recognize_google(audio).lower()
#                 print(f"You said: {command}")
#
#                 yield command  # Yield the recognized command for processing
#             except sr.UnknownValueError:
#                 print("Sorry, I didn't understand that.")
#             except sr.RequestError:
#                 print("Sorry, there was an issue connecting to the service.")
#                 break
#
# def on_key_press1():
#     # Streaming the recognized text
#     for command in process_voice_command():
#         if "run" in command or "execute" in command or "open" in command or "start" in command:
#             if "finder" in command and ("don't" or "not") not in command:
#                 os.system("open /System/Library/CoreServices/Finder.app")
#             elif "textedit" in command and ("don't" or "not") not in command:
#                 os.system("open -a TextEdit")
#             elif "safari" in command and ("don't" or "not") not in command:
#                 os.system("open -a Safari")
#             elif "chrome" in command and ("don't" or "not") not in command:
#                 os.system("open -a 'Google Chrome'")
#             elif "calculator" in command and ("don't" or "not") not in command:
#                 os.system("open -a Calculator")
#             else:
#                 print("Command not supported.")
#
#         elif "goodbye" in command:
#             print("Goodbye! Have a great day!")
#             quit()  # Exit the program
#
#         elif "stop" in command:
#             print("Stopping the voice recognition system.")
#             quit()  # Exit the program
#
#         else:
#             print("Command not supported.")

def main():
    """Main function"""
    try:
        app()
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        handle_global_error(type(e), e, sys.exc_info()[2])
        sys.exit(1)

if __name__ == '__main__':
    main()
