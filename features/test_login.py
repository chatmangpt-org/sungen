"""Login feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features/login.feature', 'Successful login')
def test_successful_login():
    """Successful login."""


@given('I am on the login page')
def _():
    """I am on the login page."""
    raise NotImplementedError


@when('I click the login button')
def _():
    """I click the login button."""
    raise NotImplementedError


@when('I enter my username and password')
def _():
    """I enter my username and password."""
    raise NotImplementedError


@then('I should be logged in successfully')
def _():
    """I should be logged in successfully."""
    raise NotImplementedError

