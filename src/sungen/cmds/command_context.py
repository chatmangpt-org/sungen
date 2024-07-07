import sys
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CommandContext:
    model: str = "gpt-4-0613"
    input: Optional[str] = None
    output: Optional[str] = None
    in_n_out: Optional[str] = None
    prompt: Optional[str] = None
    verbose: bool = False
    no_copy: bool = False
    paste: bool = False
    example: Optional[str] = None
    template: Optional[str] = None
    clear_history: bool = False
    auto_output: bool = False
    text: Optional[str] = ""
    auto_summarize: int = 4
    tokens: Optional[str] = None
    extension: Optional[str] = None
    response: Optional[str] = ""
    dsl: Optional[str] = None
    system_prompt: Optional[str] = None
    schema: Optional[str] = None
    append: Optional[str] = None


def create_context(params: dict[str, Any]) -> CommandContext:
    if str(params.get("model")) == "3":
        params["model"] = "gpt-3.5-turbo-0613"

    if str(params.get("model")) == "4":
        params["model"] = "gpt-4-0613"

    in_n_out = params.get("in_n_out")
    if in_n_out:
        params["input"] = in_n_out
        params["output"] = in_n_out

    # Add standard input to text
    # if sys.stdin.read():
    #     params['text'] += sys.stdin.read()

    if params.get("text") is None:
        params["text"] = ""

    return CommandContext(**params)
