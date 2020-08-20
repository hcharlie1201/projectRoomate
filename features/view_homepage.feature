Feature: view the home page

    As a new user,
    I should be able to see a page with login and sign up button
    So that I can sign in or sign up.

    Scenario: Viewing the home page
        Given I am on the home page
        Then I should see "Login"
        And I should see "Sign Up"