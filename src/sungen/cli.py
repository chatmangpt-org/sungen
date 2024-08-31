import typer
from rich import print
from sungen.utils.cli_tools import load_commands
from sungen.utils.file_tools import source_dir
import speech_recognition as sr
import os

app = typer.Typer()

load_commands(app, source_dir("cmds"))

@app.command()
def fire(name: str = "Chell") -> None:
    """Fire portal gun."""
    print(f"[bold red]Alert![/bold red] {name} fired [green]portal gun[/green] :boom:")
    on_key_press1()


def process_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise

        # Loop to continuously listen and recognize speech
        while True:
            try:
                print("Listening for a command...")
                audio = recognizer.listen(source, phrase_time_limit=5)  # Listen for a maximum of 5 seconds per phrase

                # Recognize the audio and convert it to text
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                yield command  # Yield the recognized command for processing
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that.")
            except sr.RequestError:
                print("Sorry, there was an issue connecting to the service.")
                break

def on_key_press1():
    # Streaming the recognized text
    for command in process_voice_command():
        if "run" in command or "execute" in command or "open" in command or "start" in command:
            if "finder" in command and ("don't" or "not") not in command:
                os.system("open /System/Library/CoreServices/Finder.app")
            elif "textedit" in command and ("don't" or "not") not in command:
                os.system("open -a TextEdit")
            elif "safari" in command and ("don't" or "not") not in command:
                os.system("open -a Safari")
            elif "chrome" in command and ("don't" or "not") not in command:
                os.system("open -a 'Google Chrome'")
            elif "calculator" in command and ("don't" or "not") not in command:
                os.system("open -a Calculator")
            else:
                print("Command not supported.")

        elif "goodbye" in command:
            print("Goodbye! Have a great day!")
            quit()  # Exit the program

        elif "stop" in command:
            print("Stopping the voice recognition system.")
            quit()  # Exit the program

        else:
            print("Command not supported.")


 
def main():
    """Main function"""

if __name__ == '__main__':
    main()
