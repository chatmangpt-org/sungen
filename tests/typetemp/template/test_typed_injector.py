import tempfile
from collections import namedtuple
from dataclasses import dataclass

import pytest
from faker import Faker

from sungen.typetemp.template.typed_injector import TypedInjector
from sungen.typetemp.template.typed_template import TypedTemplate


@dataclass
class ComplexMultiLineTemplate(TypedTemplate):
    class_name: str = None
    attributes: list = None
    methods: list = None

    source = """class {{ class_name }}:
    def __init__(self{% for attr in attributes %}, {{ attr.name }}: {{ attr.type }}{% endfor %}):
        {% for attr in attributes -%}
        self.{{ attr.name }} = {{ attr.name }}
        {% endfor %}
    {%- for method in methods %}
    def {{ method.name }}(self{% for param in method.params %}, {{ param.name }}: {{ param.type }}{% endfor %}):
        return "{{ faker_sentence() }}"  # Simulating logic with Faker sentence{% endfor %}"""


@pytest.fixture
def rendered_complex_multiline_template():
    faker = Faker()
    Attribute = namedtuple("Attribute", ["name", "type"])
    Method = namedtuple("Method", ["name", "params"])
    Param = namedtuple("Param", ["name", "type"])

    attributes = [Attribute(name=faker.word(), type=faker.word()) for _ in range(3)]
    methods = [
        Method(
            name=faker.word(),
            params=[Param(name=faker.word(), type=faker.word()) for _ in range(2)],
        )
        for _ in range(3)
    ]

    template = ComplexMultiLineTemplate(
        class_name=faker.word().capitalize(), attributes=attributes, methods=methods
    )

    return template()


@dataclass
class AfterInjectHelloWorld(TypedInjector):
    place: str
    to: str

    source = "    Hello {{ place }}!"
    after = "__init__"


def test_inject_after_init_method(rendered_complex_multiline_template):
    # Write rendered template to a temporary file
    target_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    target_file.write(rendered_complex_multiline_template)
    target_file.seek(0)

    # Inject content after the __init__ method
    injector = AfterInjectHelloWorld(to=target_file.name, place="World")
    injector.inject()

    target_file.seek(0)
    content = target_file.read()
    lines = content.split("\n")
    assert lines[2] == injector.output


@dataclass
class BeforeInjectHelloWorld(TypedInjector):
    place: str
    to: str

    source = '    """Hello {{ place }}!"""'
    before = "__init__"


def test_inject_before_init_method(rendered_complex_multiline_template):
    # Write rendered template to a temporary file
    target_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    target_file.write(rendered_complex_multiline_template)
    target_file.seek(0)

    # Inject content before the __init__ method
    injector = BeforeInjectHelloWorld(to=target_file.name, place="World")
    injector.inject()

    target_file.seek(0)
    content = target_file.read()
    lines = content.split("\n")
    assert lines[1] == injector.output


@dataclass
class AtInjectHelloWorld(TypedInjector):
    place: str
    to: str

    source = """    def {{ place }}():
        return 'hello {{ place }}!'"""
    at_line = 6


def test_inject_at_line(rendered_complex_multiline_template):
    # Write rendered template to a temporary file
    target_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    target_file.write(rendered_complex_multiline_template)
    target_file.seek(0)

    # Inject "Hello World!" at line 6
    injector = AtInjectHelloWorld(to=target_file.name, place="World")
    injector.inject()
    inj_lines = injector.output.split("\n")

    target_file.seek(0)
    lines = target_file.readlines()
    assert lines[injector.at_line - 1] == inj_lines[0] + "\n"
    assert lines[injector.at_line] == inj_lines[1] + "\n"


@dataclass
class SkipInjectHelloWorld(TypedInjector):
    place: str
    to: str

    source = "    Hello {{ place }}!"
    before = "__init__"
    skip_if = "__init__"


def test_inject_skip_if_exists(rendered_complex_multiline_template):
    # Write rendered template to a temporary file
    target_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    target_file.write(rendered_complex_multiline_template)
    target_file.seek(0)

    # Inject content but skip if pattern exists
    injector = SkipInjectHelloWorld(to=target_file.name, place="World")
    injector.inject()

    target_file.seek(0)
    content = target_file.read()
    assert content == rendered_complex_multiline_template


@dataclass
class PrependInjectHelloWorld(TypedInjector):
    place: str
    to: str

    source = "from hello import {{ place }}"
    prepend = True


def test_inject_prepend(rendered_complex_multiline_template):
    # Write rendered template to a temporary file
    target_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    target_file.write(rendered_complex_multiline_template)
    target_file.seek(0)

    # Inject content at the beginning of the file
    injector = PrependInjectHelloWorld(to=target_file.name, place="World")
    injector.inject()

    target_file.seek(0)
    content = target_file.read()
    lines = content.split("\n")
    assert lines[0] == injector.output


@dataclass
class AppendInjectHelloWorld(TypedInjector):
    place: str
    to: str

    source = """def {{ place }}():
    return 'hello {{ place }}!'"""
    append = True


def test_inject_append(rendered_complex_multiline_template):
    # Write rendered template to a temporary file
    target_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    target_file.write(rendered_complex_multiline_template)
    target_file.seek(0)

    # Inject content at the end of the file
    injector = AppendInjectHelloWorld(to=target_file.name, place="world")
    injector.inject()

    target_file.seek(0)
    content = target_file.read()
    lines = content.split("\n")

    inj_lines = injector.output.split("\n")

    assert lines[-2] == inj_lines[0]
    assert lines[-1] == inj_lines[1]
