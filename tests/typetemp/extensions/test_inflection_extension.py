import pytest
from jinja2 import Environment

from sungen.typetemp.extension.inflection_extension import InflectionExtension

# Define the test cases
test_cases = {
    "camelize": ("first_name", "FirstName"),
    "dasherize": ("first_name", "first-name"),
    "humanize": ("employee_id", "Employee"),
    "ordinal": (1, "st"),
    "ordinalize": (1, "1st"),
    "parameterize": ("Hello World!", "hello-world"),
    "pluralize": ("child", "children"),
    "singularize": ("children", "child"),
    "tableize": ("RawFirm", "raw_firms"),
    "titleize": ("man from the boondocks", "Man From The Boondocks"),
    "transliterate": ("München", "Munchen"),
    "underscore": ("FirstName", "first_name"),
}

# Initialize Jinja2 environment with InflectionExtension
env = Environment(extensions=[InflectionExtension])


@pytest.mark.parametrize("filter_name, test_data", test_cases.items())
def test_inflection_extension(filter_name, test_data):
    input, expected_output = test_data
    # Get the filter function from the environment
    filter_func = env.filters.get(filter_name)
    # If the filter exists, test it
    if filter_func:
        assert filter_func(input) == expected_output
    else:
        pytest.fail(f"Filter '{filter_name}' not found in the environment.")
