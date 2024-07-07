import pytest

from sungen.typetemp.environment.typed_environment import TypedEnvironment


def test_typed_environment_faker_extension_1():
    env = TypedEnvironment()
    template = env.from_string("{{ faker_name() }}")
    result = template.render()
    assert isinstance(result, str)


def test_typed_environment_inflection_extension_1():
    env = TypedEnvironment()
    template = env.from_string("{{ animal | pluralize }}")
    result = template.render(animal="cat")
    assert result == "cats"


def test_typed_environment_debug_extension():
    env = TypedEnvironment()
    # The debug extension provides a 'debug' statement that dumps the current context variables.
    # It won't affect our output in this simple case.
    template = env.from_string("{% debug %}{{ foo }}")
    result = template.render(foo="bar")
    assert result.startswith("{'context'")


def test_typed_environment_do_extension():
    env = TypedEnvironment()
    # The 'do' extension allows assignments in expressions, which normally isn't possible
    # It won't affect our output in this simple case.
    template = env.from_string("{% do list.append('c') %}{{ list }}")
    result = template.render(list=["a", "b"])
    assert result == "['a', 'b', 'c']"


def test_typed_environment_loopcontrols_extension():
    env = TypedEnvironment()
    # The loopcontrols extension provides break and continue statements in loops
    # If we encounter 'b', we break the loop and stop output
    template = env.from_string(
        "{% for letter in list %}{% if letter == 'b' %}{% break %}{% endif %}{{ letter }}{% endfor %}"
    )
    result = template.render(list=["a", "b", "c"])
    assert result == "a"
