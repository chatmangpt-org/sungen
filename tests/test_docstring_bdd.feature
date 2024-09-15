
Feature: Counter
    A simple counter that can be incremented.

    Scenario: Incrementing the counter
        Given the counter is at 0
        When I increment the counter by 1
        Then the counter should be 1

        When I increment the counter by 2
        Then the counter should be 3
