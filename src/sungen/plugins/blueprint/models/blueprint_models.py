from pydantic import  Field
from typing import List, Optional

from dslmodel import DSLModel


class AiderBlueprint(DSLModel):
    """Defines a Blueprint for using Aider."""
    module_name: str = Field(..., description="Name of the blueprint module.")
    version: str = Field(default="1.0.0", description="Version of the blueprint.")
    verbose: bool = Field(default=False, description="Enable or disable verbose output.")
    description: str = Field(..., description="Description of the blueprint.")
    files_to_create: List[str] = Field(..., description="List of files to be created.")
    files_to_edit: List[str] = Field(..., description="List of files to be edited.")
    read_only_files: List[str] = Field(default_factory=list, description="List of files to be marked as read-only.")
    model: str = Field(default="gpt-4o-mini", description="AI model to use.")
    auto_test: bool = Field(default=True, description="Enable or disable automatic testing after edits.")
    lint: bool = Field(default=True, description="Enable or disable linting of files.")
    auto_commit: bool = Field(default=False, description="Enable or disable automatic commits.")
    additional_args: Optional[List[str]] = Field(default_factory=list, description="Additional command-line arguments for Aider.")
    message: str = Field(None, description="Custom message to use for the Aider command.")
    context_files: List[str] = Field(default_factory=list, description="List of relevant context files.")


class CodeBlueprint(DSLModel):
    """
    Defines a blueprint for configuring and running commands with code generation tools in an enterprise environment.

    This class encapsulates configuration parameters for creating, editing, and managing files using AI-powered development assistants or code generation tools. It supports versioning, compliance checks, integration points, and various strategies to ensure scalability and security in development workflows.

    By defining this blueprint, organizations can enforce standardized development practices, automate workflows, ensure security compliance, and optimize resource management across projects.
    """
    module_name: str = Field(
        ...,
        description="Name of the blueprint module, representing the specific feature or functionality "
                    "this blueprint is designed to support."
    )
    version: str = Field(
        default="1.0.0",
        description="Version of the blueprint, useful for tracking changes or updates to the configuration."
    )
    verbose: bool = Field(
        default=False,
        description="Enable or disable verbose output from the code generation tool. "
                    "When enabled, detailed logs of operations are provided, which can help in debugging."
    )
    description: str = Field(
        ...,
        description="Description of the blueprint, explaining its purpose, functionality, "
                    "and how it is intended to be used."
    )
    files_to_create: List[str] = Field(
        ...,
        description="List of files that should be created as part of this blueprint. "
                    "The tool will ensure these files exist before proceeding with any operations."
    )
    files_to_edit: List[str] = Field(
        ...,
        description="List of files that the code generation tool will edit. "
                    "These files are the focus of the tool's modifications or enhancements."
    )
    read_only_files: List[str] = Field(
        default_factory=list,
        description="List of files to be marked as read-only. The tool will consider these files for context "
                    "but will not modify them. Useful for providing additional information without risking unwanted changes."
    )
    model: str = Field(
        default="gpt-4o-mini",
        description="AI model or engine to use. Determines the language model the tool will interact with. "
                    "Defaults to 'gpt-4o-mini', but can be set to any other supported model."
    )
    test_cmd: Optional[str] = Field(
        None,
        description="Command to run tests after edits. If provided, the tool will automatically run this command "
                    "after making changes to ensure they do not introduce errors."
    )
    lint: bool = Field(
        default=True,
        description="Enable or disable linting of files. When enabled, the tool will run a linter on the "
                    "specified files to check for and correct code style and syntax issues."
    )
    auto_commit: bool = Field(
        default=False,
        description="Enable or disable automatic commits of changes made by the tool. "
                    "When enabled, the tool will automatically commit changes to the version control system."
    )
    additional_args: Optional[List[str]] = Field(
        default_factory=list,
        description="Additional command-line arguments for the tool. These can be any extra options or flags "
                    "that are not explicitly covered by the other attributes of the blueprint."
    )
    message: str = Field(
        None,
        description="Custom message to use for the tool's operations. Useful for providing a specific instruction "
                    "or context for the tool to consider when making changes."
    )
    context_files: List[str] = Field(
        default_factory=list,
        description="List of relevant context files. These files are included as additional context for the tool, "
                    "helping it understand the broader codebase or environment without being modified."
    )