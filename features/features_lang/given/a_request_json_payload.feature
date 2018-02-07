Feature: Step given a request json payload
    Validates the functionality of the given step "a request json payload"


    Scenario: Sets the specified payload in the context
        Given a request json payload
            """
            {
                "id": 1,
                "name": "resource name"
            }
            """
        Then the context request json payload is equal to
            """
            {
                "id": 1,
                "name": "resource name"
            }
            """


    Scenario: Resolves variables in the payload
        Given a request json payload
            """
            {
                "id": ${OBJECT_ID},
                "name": "${RESOURCE_NAME}"
            }
            """
        Then the context request json payload is equal to
            """
            {
                "id": 3,
                "name": "resolved name"
            }
            """


