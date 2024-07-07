# Here is your PerfectPythonProductionPEP8® AGI code you requested:
from dataclasses import dataclass

from sungen.typetemp.template.typed_template import TypedTemplate


# To integrate this mixin into your existing TypedTemplate class, you'd do something like this:
@dataclass
class NewTypedTemplate(TypedTemplate):
    name: str = None
    source = "Hello, {{ name }}"


# Test the render() function
def test_render_mixin():
    # Initialize a NewTypedTemplate object
    template = NewTypedTemplate(name="John")

    # Render the template with a name variable
    output = template._render(name="John")

    # Assert that the output is as expected
    assert output == "Hello, John"
    assert template.output == "Hello, John"
