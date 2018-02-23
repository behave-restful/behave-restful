Feature: Step then the response json matches defined schema
    Validates the functionality of the step "the response json matches defined schema"

    Background: We use a response double from where the JSON payload is retrieved
        Given a test response
            And the response contains a json body like
                """
                {
                    "id": 1,
                    "name": "a name"
                }
                """


    Scenario: Validates the response against the specified schema id
        Then the response json matches defined schema TEST_SCHEMA


    Scenario: Resolves the schema id to retrieve the defined schema
        Then the response json matches defined schema ${TEST_SCHEMA_ID}