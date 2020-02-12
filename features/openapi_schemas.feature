Feature: Schema Validation from OpenAPI Schemas
    This feature allows to validate responses using the schemas defined in an
    OpenAPI document.


    Scenario: Can validate a response using a JSON based OpenAPI file
        Given an openapi file ${WORKING_DIR}/data/openapi/openapi.json
            And a test response
            And the response contains a json body like
                """
                {
                    "items": [
                        {
                            "id": "45321",
                            "title": "Sultans of Swing",
                            "artist": {
                                "name": "Dire Straits"
                            }
                        }
                    ]
                }
                """
        Then the response json matches defined schema SongCollection


    Scenario: Can validate a response using a YAML based OpenAPI file
        Given an openapi file ${WORKING_DIR}/data/openapi/openapi.yaml
            And a test response
            And the response contains a json body like
                """
                {
                    "items": [
                        {
                            "id": "45321",
                            "title": "Sultans of Swing",
                            "artist": {
                                "name": "Dire Straits"
                            }
                        }
                    ]
                }
                """
        Then the response json matches defined schema SongCollection