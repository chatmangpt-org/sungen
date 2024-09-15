Dynamic Feature Generation:

Extract module-level docstring.
Convert docstring to .feature file.
Store feature file in the same directory as the Python script.
Single Source of Truth:

Feature descriptions and scenarios defined in Python docstring.
Centralized updates reduce duplication and errors.
Function: docstring_to_feature_file:

Input: Python module object.
Output: Path to the .feature file.
Process:
Retrieve docstring.
Write to .feature file.
Raise error if no docstring found.
Function: scenario_path:

Input: module_name.
Output: Path to .feature file.
Process:
Fetch module from sys.modules.
Call docstring_to_feature_file.
BDD Integration:

Use pytest-bdd scenarios function.
Dynamically link .feature file path using scenario_path.
Automation Benefits:

Consistency: Keeps feature files synchronized with tests.
Efficiency: Automatically generates feature files, minimizing manual steps.
Simplicity: Centralized docstrings maintain documentation directly in test files.
Usage:

Write feature description in the module-level docstring.
Run tests with pytest.
Feature files dynamically generated; tests executed.
Key Concepts:

Dynamic Linking: Link scenarios to dynamically created feature files.
Automated Validation: Automatically validate scenarios with pytest-bdd.
Centralized Maintenance: Maintain feature descriptions and scenarios directly in Python files.
Example Structure:

Python script contains Gherkin-formatted docstring.
pytest-bdd scenarios function registers scenarios using scenario_path.
Result:

Simplified BDD workflow.
Single-point updates for feature scenarios.
Reduced duplication and management overhead.

"""
Feature: Counter
    A simple counter that can be incremented.

    Scenario: Incrementing the counter
        Given the counter is at 0
        When I increment the counter by 1
        Then the counter should be 1

        When I increment the counter by 2
        Then the counter should be 3
"""

from pytest_bdd import given, when, then, parsers, scenarios
import pytest
from conftest import scenario_path  # Import the custom scenarios wrapper

scenarios(scenario_path(__name__))

@pytest.fixture
def counter():
    return {"value": 0}

@given("the counter is at 0", target_fixture="counter")
def counter_at_zero():
    return {"value": 0}

@when(parsers.parse("I increment the counter by {amount:d}"))
def increment_counter(counter, amount):
    counter["value"] += amount

@then(parsers.parse("the counter should be {expected:d}"))
def counter_should_be(counter, expected):
    assert counter["value"] == expected
