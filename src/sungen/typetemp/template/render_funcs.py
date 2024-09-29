from typing import Any

import jinja2

from ..environment.typed_environment import async_environment, environment
from ..environment.typed_native_environment import (
    async_native_environment,
    native_environment,
)


def render_str(source, **kwargs) -> str:
    """
    Render a template string with the given context.

    :param source: Template string.
    :param kwargs: Context variables to render the template. 'dest' is a special keyword argument that specifies the destination file path.
    :return: Rendered template as a string.
    """
    dest = kwargs.pop('dest', None)  # Check for 'dest' in kwargs
    try:
        template = environment.from_string(source)
    except jinja2.exceptions.TemplateSyntaxError as e:
        print(f"Error processing template: {e}")
        print(f"Problematic template string: {source}")
        raise
    
    rendered_content = template.render(**kwargs)
    
    if dest:  # If 'dest' is provided, write the rendered content to disk
        with open(dest, 'w') as file:
            file.write(rendered_content)
    
    return rendered_content

async def arender_str(source, **kwargs) -> str:
    template = async_environment.from_string(source)

    return await template.render_async(**kwargs)


def render_py(source, env=native_environment, **kwargs) -> Any:
    template = env.from_string(source)

    return template.render(**kwargs)


async def arender_py(source, env=async_native_environment, **kwargs) -> Any:
    template = env.from_string(source)

    return await template.render_async(**kwargs)


def render_file(template_path: str, **kwargs) -> str:
    """
    Load a template from a file and render it with the given context.

    :param template_path: Path to the template file.
    :param kwargs: Context variables to render the template. 'dest' is a special keyword argument that specifies the destination file path.
    :return: Rendered template as a string.
    """
    try:
        with open(template_path, 'r') as file:
            source = file.read()
        return render_str(source, **kwargs)
    except FileNotFoundError:
        print(f"Template file not found: {template_path}")
        raise
    except Exception as e:
        print(f"Error rendering template: {e}")
        raise
