Feature: Step then the response status is
    Validates the functionality of the then step "the response status is"

    Background: We use a response double from where the status will be validated
        Given a test response
            And a response status of 404


    Scenario: Supports specifying expected status as numeric
        Then the response status is 404


    Scenario: Support specifying the expected status as constant name
        Then the response status is NOT_FOUND


    Scenario: Supports specifying the expected status with spaces
        Then the response status is NOT FOUND


    Scenario: Supportss specifying the expected status with any casing
        Then the response status is Not found

    