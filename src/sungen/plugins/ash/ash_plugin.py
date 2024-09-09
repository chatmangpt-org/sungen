import typer
import subprocess
from typing import Optional
from sungen.utils.plugin_tools import load_plugin_config, validate_plugin_compatibility
from sungen.utils.chat_tools import chatbot

app = typer.Typer(help="Ash Studio Ecosystem Plugin for Elixir development", name="ash")

def run_chatbot(question, context):
    return chatbot(question, context)

@app.command()
def init(project_name: str):
    """Initialize a new Ash Studio project"""
    context = f"Initializing a new Ash Studio project named '{project_name}'"
    chat_response = run_chatbot(f"How to initialize an Ash Studio project named {project_name}?", context)
    
    try:
        subprocess.run(["mix", "archive.install", "hex", "ash_studio"], check=True)
        subprocess.run(["ash_studio", "init", project_name], check=True)
        typer.echo(f"Successfully initialized Ash Studio project: {project_name}")
        typer.echo("\nChatbot assistance:")
        typer.echo(chat_response)
        typer.echo("\nImplementation instructions:")
        typer.echo("1. Review the generated project structure, focusing on the 'lib' and 'config' directories.")
        typer.echo("2. Customize the 'config/config.exs' file to set up your database and other environment-specific settings.")
        typer.echo("3. Define your domain entities as Ash resources in the 'lib/your_app/resources' directory.")
        typer.echo("4. Set up authentication and authorization using Ash Authentication and Ash Policy Authorizer.")
        typer.echo("5. Configure your API layer using Ash JSON:API or Ash GraphQL based on your project requirements.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Failed to initialize Ash Studio project: {str(e)}")
        chat_response = run_chatbot(f"How to troubleshoot Ash Studio project initialization failure: {str(e)}", context)
        typer.echo("\nChatbot troubleshooting assistance:")
        typer.echo(chat_response)

@app.command()
def generate(entity_type: str, name: str, attributes: Optional[str] = None):
    """Generate Ash resources, actions, or policies"""
    context = f"Generating Ash {entity_type} named '{name}' with attributes: {attributes}"
    chat_response = run_chatbot(f"How to generate an Ash {entity_type} named {name} with attributes: {attributes}?", context)
    
    try:
        cmd = ["ash_studio", "generate", entity_type, name]
        if attributes:
            cmd.extend(["--attributes", attributes])
        subprocess.run(cmd, check=True)
        typer.echo(f"Successfully generated {entity_type}: {name}")
        typer.echo("\nChatbot assistance:")
        typer.echo(chat_response)
        typer.echo("\nImplementation instructions:")
        typer.echo(f"1. Locate the generated {entity_type} file in the appropriate directory (e.g., 'lib/your_app/resources' for resources).")
        typer.echo(f"2. Review and customize the generated {entity_type} definition, adding any necessary relationships or constraints.")
        typer.echo("3. If generating a resource, define appropriate actions (create, read, update, destroy) and their corresponding policies.")
        typer.echo("4. For custom actions, implement the action logic in the resource file and define any necessary inputs and outputs.")
        typer.echo("5. Update your API layer (JSON:API or GraphQL) to expose the new resource or action if required.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Failed to generate {entity_type}: {str(e)}")
        chat_response = run_chatbot(f"How to troubleshoot Ash {entity_type} generation failure: {str(e)}", context)
        typer.echo("\nChatbot troubleshooting assistance:")
        typer.echo(chat_response)

@app.command()
def migrate():
    """Manage database migrations for Ash resources"""
    context = "Running Ash migrations"
    chat_response = run_chatbot("What are the best practices for running Ash migrations?", context)
    
    try:
        subprocess.run(["mix", "ash.migrate"], check=True)
        typer.echo("Successfully ran Ash migrations")
        typer.echo("\nChatbot assistance:")
        typer.echo(chat_response)
        typer.echo("\nImplementation instructions:")
        typer.echo("1. Review the generated migration files in the 'priv/repo/migrations' directory to ensure they reflect your intended changes.")
        typer.echo("2. Test the migrations in a staging environment before applying them to production.")
        typer.echo("3. Implement a rollback strategy for each migration in case of unexpected issues.")
        typer.echo("4. Consider using Ash's built-in versioning system for managing resource changes over time.")
        typer.echo("5. After running migrations, verify the database schema and perform thorough testing of affected resources and actions.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Failed to run Ash migrations: {str(e)}")
        chat_response = run_chatbot(f"How to troubleshoot Ash migration failure: {str(e)}", context)
        typer.echo("\nChatbot troubleshooting assistance:")
        typer.echo(chat_response)

@app.command()
def start():
    """Run the Ash Studio application server"""
    context = "Starting the Ash Studio application server"
    chat_response = run_chatbot("What should I know before starting the Ash Studio application server?", context)
    
    typer.echo("Chatbot advice before starting the server:")
    typer.echo(chat_response)
    typer.echo("\nImplementation instructions:")
    typer.echo("1. Ensure all environment variables are properly set, including database credentials and API keys.")
    typer.echo("2. Verify that all required dependencies are installed and up-to-date.")
    typer.echo("3. Run any pending migrations before starting the server to ensure database schema consistency.")
    typer.echo("4. Consider implementing a pre-start hook to perform any necessary setup or validation tasks.")
    typer.echo("5. Monitor the server logs carefully during startup for any warnings or errors that may require attention.")
    
    try:
        subprocess.run(["mix", "phx.server"], check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Failed to start Ash Studio server: {str(e)}")
        chat_response = run_chatbot(f"How to troubleshoot Ash Studio server start failure: {str(e)}", context)
        typer.echo("\nChatbot troubleshooting assistance:")
        typer.echo(chat_response)

@app.command()
def validate():
    """Validate the Ash Studio project configuration"""
    context = "Validating Ash Studio project configuration"
    chat_response = run_chatbot("What are important aspects to check when validating an Ash Studio project configuration?", context)
    
    try:
        config = load_plugin_config("plugin.yaml")
        current_version = "1.0.0"  # Replace with actual version retrieval
        is_compatible = validate_plugin_compatibility(config, current_version)
        
        if is_compatible:
            typer.echo("Ash Studio project configuration is valid and compatible.")
        else:
            typer.echo("Ash Studio project configuration is not compatible with the current version.")
        
        typer.echo("\nChatbot assistance on configuration validation:")
        typer.echo(chat_response)
        typer.echo("\nImplementation instructions:")
        typer.echo("1. Review all resource definitions to ensure they follow Ash best practices and naming conventions.")
        typer.echo("2. Verify that all relationships between resources are correctly defined and configured.")
        typer.echo("3. Check the consistency of policies across resources and actions to maintain proper access control.")
        typer.echo("4. Validate the API layer configuration (JSON:API or GraphQL) to ensure all intended resources and actions are exposed.")
        typer.echo("5. Run comprehensive tests, including unit tests for resources and integration tests for the API layer.")
    except Exception as e:
        typer.echo(f"Failed to validate Ash Studio project: {str(e)}")
        chat_response = run_chatbot(f"How to troubleshoot Ash Studio project validation failure: {str(e)}", context)
        typer.echo("\nChatbot troubleshooting assistance:")
        typer.echo(chat_response)

@app.command()
def info():
    """Display information about the Ash Studio project"""
    context = "Displaying Ash Studio project information"
    chat_response = run_chatbot("What key information should be checked in an Ash Studio project?", context)
    
    try:
        config = load_plugin_config("plugin.yaml")
        typer.echo(f"Ash Studio Ecosystem Plugin")
        typer.echo(f"Version: {config.version}")
        typer.echo(f"Description: {config.description}")
        typer.echo(f"Supported Elixir version: {config.elixir_version}")
        typer.echo(f"Supported Ash version: {config.ash_version}")
        
        typer.echo("\nChatbot insights on project information:")
        typer.echo(chat_response)
        typer.echo("\nImplementation instructions:")
        typer.echo("1. Regularly review and update the project's dependencies to ensure compatibility and security.")
        typer.echo("2. Maintain comprehensive documentation of your Ash resources, actions, and policies for easy reference.")
        typer.echo("3. Implement a versioning strategy for your API to manage changes and maintain backward compatibility.")
        typer.echo("4. Set up monitoring and observability tools to track the performance and health of your Ash application.")
        typer.echo("5. Establish a clear process for contributing to and reviewing changes in the project to maintain code quality and consistency.")
    except Exception as e:
        typer.echo(f"Failed to retrieve Ash Studio project information: {str(e)}")
        chat_response = run_chatbot(f"How to troubleshoot Ash Studio project information retrieval failure: {str(e)}", context)
        typer.echo("\nChatbot troubleshooting assistance:")
        typer.echo(chat_response)

def register_plugin(parent_app: typer.Typer):
    """Register the plugin with the main application."""
    try:
        parent_app.add_typer(app)
    except Exception as e:
        print(f"Failed to register plugin '{app}': {str(e)}")

if __name__ == "__main__":
    app()
