Feature: Step when request sends
    Validates the functionality of the when step "the request sends"

    Background: We use a session double to validate the request
        Given a test session
            And a request url http://my.server.com/api/resource
            And a request json payload
                """
                {
                    "id": 13,
                    "name": "the object"
                }
                """


    Scenario: Supports get requests
        When the request sends get
        Then the session get_invoked property is True


    Scenario: Supports post requests
        When the request sends post
        Then the session post_invoked property is True


    Scenario: Supports put requests
        When the request sends put
        Then the session put_invoked property is True


    Scenario: Supports delete requests
        When the request sends delete
        Then the session delete_invoked property is True


    Scenario: Method name can have any capitalization
        When the request sends Put
        Then the session put_invoked property is True