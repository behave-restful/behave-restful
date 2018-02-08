Feature: Step then the response json matches
    Validates the functionality of the step "the response json matches"

    Background: We use a response double from where the JSON payload is retrieved.
        Given a test response
            And the response contains a json body like
                """
                {
                    "id": 1,
                    "name": "a name"
                }
                """


    Scenario: Validates the response against specified schema
        Then the response json matches
            """
            {
                "title": "SampleObject",
                "type": "object",
                "properties": {
                    "id": {"type": "number"},
                    "name": {"type": "string"}
                },
                "required": ["id", "name"]
            }
            """

    Scenario: Supports specifying variables in the schema
        Then the response json matches
            """
            {
                "title": "SampleObject",
                "type": "object",
                "properties": {
                    "id": ${TYPE_NUMBER},
                    "name": ${TYPE_STRING}
                },
                "${REQUIRED}": ["id", "name"]
            }
            """