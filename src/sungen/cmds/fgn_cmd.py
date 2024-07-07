"""fgn"""
import typer


app = typer.Typer()


@app.command(name="blog")
def _blog():
    """blog"""
    typer.echo("Running blog subcommand.")


import typer
from typing import Optional

app = typer.Typer()


@app.command()
def fgn(
    model: str = typer.Option("gpt-4-0613", "--model", "-m", help="The OpenAI model to be used for AGI response."),
    input: Optional[str] = typer.Option(None, "--input", "-i", help="Path to input file."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Path to output file."),
    in_n_out: Optional[str] = typer.Option(None, "--in-n-out", "-io", help="Path to input and output file."),
    prompt: Optional[str] = typer.Option(None, "--prompt", "-pr", help="Prompt itself as a string."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose mode for printing output."),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Path to template file."),
    example: Optional[str] = typer.Option(None, "--example", "-e", help="Path to example file."),
    system_prompt: Optional[str] = typer.Option(None, "--system-prompt", "-sp", help="Path to system prompt file."),
    schema: Optional[str] = typer.Option(None, "--schema", "-sc", help="Path to response schema definition file."),
    clear_history: bool = typer.Option(False, "--clear-history", help="Clear the history file."),
    auto_output: bool = typer.Option(False, "--auto-output", "-ao", help="Automatically output to file with automatic file name."),
    auto_summarize: int = typer.Option(4, "--auto-summarize", "-as", help="Automatic summarization after the specified number of messages."),
    paste: bool = typer.Option(False, "--paste", "-p", help="Paste input from the clipboard."),
    no_copy: bool = typer.Option(False, "--no-copy", "-nc", help="Do not copy output to the clipboard."),
    tokens: Optional[str] = typer.Option(None, "--tokens", "-tk", help="Token replacement separated by ;"),
    extension: Optional[str] = typer.Option(None, "--extension", "-ext", help="File extension of auto output file."),
    dsl: Optional[str] = typer.Option(None, "--dsl", "-d", help="Use the FGN Domain Specific Language."),
    append: bool = typer.Option(False, "--append", "-a", help="Append to the output file.")
):
    ctx_params = {
        "model": model,
        "input": input,
        "output": output,
        "in_n_out": in_n_out,
        "prompt": prompt,
        "verbose": verbose,
        "template": template,
        "example": example,
        "system_prompt": system_prompt,
        "schema": schema,
        "clear_history": clear_history,
        "auto_output": auto_output,
        "auto_summarize": auto_summarize,
        "paste": paste,
        "no_copy": no_copy,
        "tokens": tokens,
        "extension": extension,
        "dsl": dsl,
        "append": append,
    }


    if verbose:
        print(fgn_ctx)

if __name__ == "__main__":
    app()
