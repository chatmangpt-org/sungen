import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

from sungen.typetemp.template.typed_template import TypedTemplate


@dataclass
class HelloTemplate(TypedTemplate):
    name: str = None
    source = "Hello {{ name }}!"


@dataclass
class FakeTemplate(TypedTemplate):
    source = "Hello {{ faker_name() }}!"


@dataclass
class JSONTemplate(TypedTemplate):
    key: str = None
    value: str = None
    hello_dict = {"{{key}}": "{{value}}"}

    source = json.dumps(hello_dict)


def test_name():
    temp = HelloTemplate(name="World")
    assert temp() == "Hello World!"


def test_fake_name():
    temp = FakeTemplate()
    assert temp() != "Hello World!"


def test_json_source():
    temp = JSONTemplate(key="Hello", value="World")
    assert temp(use_native=True) == {"Hello": "World"}


@dataclass
class ToPropertyTemplate(TypedTemplate):
    name: str = None
    source = "Hello {{ name }}!"
    to: str = None


def test_to_property():
    user = "John"
    feature = "emails"

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        expected_to_path = temp_dir_path / f"./src/app/{feature}/{user}.html"

        expected_rendered_value = f"Hello {user}!"

        # Make sure the directory structure exists
        expected_to_path.parent.mkdir(parents=True, exist_ok=True)

        # Override the "to" property with the temporary path
        rendered = ToPropertyTemplate(name=user, to=str(expected_to_path))()

        assert rendered == expected_rendered_value

        # Check the content of the file at the rendered "to" path
        with open(expected_to_path, "r") as file:
            content = file.read()
            assert content == expected_rendered_value


class NotDataclass(TypedTemplate):
    name: str
    source = "Hello {{ name }}!"
