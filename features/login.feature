Feature: Login
  As a user
  I want to log in
  So that I can access the system

  Scenario: Successful login
    Given I am on the login page
    When I enter my username and password
    And I click the login button
    Then I should be logged in successfully