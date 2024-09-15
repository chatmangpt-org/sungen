# """
# Feature: Counter
#     A simple counter that can be incremented.
#
#     Scenario: Incrementing the counter
#         Given the counter is at 0
#         When I increment the counter by 1
#         Then the counter should be 1
#
#         When I increment the counter by 2
#         Then the counter should be 3
# """
# from pytest_bdd import given, when, then, parsers, scenarios
#
# import pytest
# from conftest import scenario_path  # Import the custom scenarios wrapper
#
# # Use the custom scenarios wrapper to handle feature file creation
# # get absolute path of the current file
# scenarios(scenario_path(__name__))
#
#
# @pytest.fixture
# def counter():
#     """A simple fixture to hold the counter value."""
#     return {"value": 0}
#
# @given("the counter is at 0", target_fixture="counter")
# def counter_at_zero():
#     """Initialize the counter to 0."""
#     return {"value": 0}
#
# @when(parsers.parse("I increment the counter by {amount:d}"))
# def increment_counter(counter, amount):
#     """Increment the counter by the given amount."""
#     counter["value"] += amount
#
# @then(parsers.parse("the counter should be {expected:d}"))
# def counter_should_be(counter, expected):
#     """Check that the counter has the expected value."""
#     assert counter["value"] == expected
