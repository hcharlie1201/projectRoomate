Feature: View Hompage

    As an anonymous user
    I want to able to see homepage that has a login button and signup button
    So that I can login or sign up

    # Background: 
    #     Given I am on the hompage
    Scenario: See the login button and the signup button
        Given I am on the home page
        Then I should see "Login"
        And I should see "Sign Up"
