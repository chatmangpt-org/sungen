from confz import BaseConfig, FileSource
from pydantic import SecretStr, AnyUrl

from pydantic import BaseModel, Field
from typing import Optional, List

class AiderConfigSchema(BaseConfig):
    # Main configuration
    openai_api_key: Optional[SecretStr] = Field(None, description="Specify the OpenAI API key")
    anthropic_api_key: Optional[SecretStr] = Field(None, description="Specify the Anthropic API key")
    model: Optional[str] = Field(None, description="Specify the model to use for the main chat")
    opus: bool = Field(False, description="Use claude-3-opus-20240229 model for the main chat")
    sonnet: bool = Field(False, description="Use claude-3-5-sonnet-20240620 model for the main chat")
    model_4: bool = Field(False, description="Use gpt-4-0613 model for the main chat")
    model_4o: bool = Field(False, description="Use gpt-4o-2024-08-06 model for the main chat")
    mini: bool = Field(False, description="Use gpt-4o-mini model for the main chat")
    model_4_turbo: bool = Field(False, description="Use gpt-4-1106-preview model for the main chat")
    model_35turbo: bool = Field(False, description="Use gpt-3.5-turbo model for the main chat")
    deepseek: bool = Field(False, description="Use deepseek/deepseek-coder model for the main chat")

    # Model settings
    list_models: Optional[bool] = Field(None, description="List known models which match the (partial) MODEL name")
    openai_api_base: Optional[str] = Field(None, description="Specify the OpenAI API base URL")
    openai_api_type: Optional[str] = Field(None, description="Specify the OpenAI API type")
    openai_api_version: Optional[str] = Field(None, description="Specify the OpenAI API version")
    openai_api_deployment_id: Optional[str] = Field(None, description="Specify the deployment ID")
    openai_organization_id: Optional[str] = Field(None, description="Specify the OpenAI organization ID")
    model_settings_file: Optional[str] = Field(None, description="Specify a file with aider model settings for unknown models")
    model_metadata_file: Optional[str] = Field(None, description="Specify a file with context window and costs for unknown models")
    verify_ssl: bool = Field(True, description="Verify the SSL cert when connecting to models")
    edit_format: Optional[str] = Field(None, description="Specify what edit format the LLM should use")
    weak_model: Optional[str] = Field(None, description="Specify the model to use for commit messages and chat history summarization")
    show_model_warnings: bool = Field(True, description="Only work with models that have meta-data available")
    map_tokens: int = Field(1024, description="Suggested number of tokens to use for repo map")
    map_refresh: Optional[str] = Field("auto", description="Control how often the repo map is refreshed")
    cache_prompts: bool = Field(False, description="Enable caching of prompts")
    cache_keepalive_pings: int = Field(0, description="Number of times to ping at 5min intervals to keep prompt cache warm")
    map_multiplier_no_files: bool = Field(True, description="Multiplier for map tokens when no files are specified")
    max_chat_history_tokens: Optional[int] = Field(None, description="Maximum number of tokens to use for chat history")
    env_file: str = Field(".env", description="Specify the .env file to load")

    # History files
    input_history_file: str = Field(".aider.input.history", description="Specify the chat input history file")
    chat_history_file: str = Field(".aider.chat.history.md", description="Specify the chat history file")
    restore_chat_history: bool = Field(False, description="Restore the previous chat history messages")
    llm_history_file: Optional[str] = Field(None, description="Log the conversation with the LLM to this file")

    # Output settings
    dark_mode: bool = Field(False, description="Use colors suitable for a dark terminal background")
    light_mode: bool = Field(False, description="Use colors suitable for a light terminal background")
    pretty: bool = Field(True, description="Enable/disable pretty, colorized output")
    stream: bool = Field(True, description="Enable/disable streaming responses")
    user_input_color: str = Field("#00cc00", description="Set the color for user input")
    tool_output_color: Optional[str] = Field(None, description="Set the color for tool output")
    tool_error_color: str = Field("#FF2222", description="Set the color for tool error messages")
    tool_warning_color: str = Field("#FFA500", description="Set the color for tool warning messages")
    assistant_output_color: str = Field("#0088ff", description="Set the color for assistant output")
    code_theme: str = Field("default", description="Set the markdown code theme")
    show_diffs: bool = Field(False, description="Show diffs when committing changes")

    # Git settings
    git: bool = Field(True, description="Enable/disable looking for a git repo")
    gitignore: bool = Field(True, description="Enable/disable adding .aider* to .gitignore")
    aiderignore: Optional[str] = Field(None, description="Specify the aider ignore file")
    subtree_only: bool = Field(False, description="Only consider files in the current subtree of the git repository")
    auto_commits: bool = Field(True, description="Enable/disable auto commit of LLM changes")
    dirty_commits: bool = Field(True, description="Enable/disable commits when repo is found dirty")
    attribute_author: bool = Field(True, description="Attribute aider code changes in the git author name")
    attribute_committer: bool = Field(True, description="Attribute aider commits in the git committer name")
    attribute_commit_message_author: bool = Field(False, description="Prefix commit messages with 'aider: ' if aider authored the changes")
    attribute_commit_message_committer: bool = Field(False, description="Prefix all commit messages with 'aider: '")
    commit: bool = Field(False, description="Commit all pending changes with a suitable commit message, then exit")
    commit_prompt: Optional[str] = Field(None, description="Specify a custom prompt for generating commit messages")
    dry_run: bool = Field(False, description="Perform a dry run without modifying files")

    # Fixing and committing
    lint: bool = Field(False, description="Lint and fix provided files, or dirty files if none provided")
    lint_cmd: Optional[List[str]] = Field(None, description="Specify lint commands to run for different languages")
    auto_lint: bool = Field(True, description="Enable/disable automatic linting after changes")
    test_cmd: Optional[str] = Field(None, description="Specify command to run tests")
    auto_test: bool = Field(False, description="Enable/disable automatic testing after changes")
    test: bool = Field(False, description="Run tests and fix problems found")

    # Other settings
    file: Optional[List[str]] = Field(None, description="Specify a file to edit")
    read: Optional[List[str]] = Field(None, description="Specify a read-only file")
    vim: bool = Field(False, description="Use VI editing mode in the terminal")
    voice_language: str = Field("en", description="Specify the language for voice using ISO 639-1 code")
    chat_language: Optional[str] = Field(None, description="Specify the language to use in the chat")
    version: Optional[bool] = Field(None, description="Show the version number and exit")
    just_check_update: bool = Field(False, description="Check for updates and return status in the exit code")
    check_update: bool = Field(True, description="Check for new aider versions on launch")
    install_main_branch: bool = Field(False, description="Install the latest version from the main branch")
    upgrade: bool = Field(False, description="Upgrade aider to the latest version from PyPI")
    apply: Optional[str] = Field(None, description="Apply the changes from the given file instead of running the chat")
    yes: bool = Field(False, description="Always say yes to every confirmation")
    verbose: bool = Field(False, description="Enable verbose output")
    show_repo_map: bool = Field(False, description="Print the repo map and exit")
    show_prompts: bool = Field(False, description="Print the system prompts and exit")
    exit: bool = Field(False, description="Do all startup activities then exit before accepting user input")
    message: Optional[str] = Field(None, description="Specify a single message to send the LLM, process reply then exit")
    message_file: Optional[str] = Field(None, description="Specify a file containing the message to send the LLM, process reply, then exit")
    encoding: str = Field("utf-8", description="Specify the encoding for input and output")
    config: Optional[str] = Field(None, description="Specify the config file")
    gui: bool = Field(False, description="Run aider in your browser")
    suggest_shell_commands: bool = Field(True, description="Enable/disable suggesting shell commands")

    CONFIG_SOURCES = FileSource(file='.aider.conf.yml')




