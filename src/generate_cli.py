import yaml
from jinja2 import Environment, FileSystemLoader

# Load the OpenAPI YAML file
with open("/Users/sac/dev/sungen/helpdesk/openapi.yaml", "r") as file:
    openapi_spec = yaml.safe_load(file)

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader(searchpath="."))

# Load the Jinja2 template
template = env.get_template("typer_template.j2")

# Render the template with the OpenAPI spec
rendered_code = template.render(openapi=openapi_spec)

# Save the generated Typer CLI code to a file
with open("/Users/sac/dev/sungen/src/helpdesk_cli.py", "w") as output_file:
    output_file.write(rendered_code)

print("Typer CLI code generated and saved to /Users/sac/dev/sungen/src/helpdesk_cli.py")
