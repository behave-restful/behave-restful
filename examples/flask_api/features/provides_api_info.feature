Feature: Provides api info

  Requests to the root of the api
  provide infp about the api itself

Scenario: Get the api version
        Given a request url http://127.0.0.1:5000
        When the request sends GET
        Then the response status is OK
            And the response json matches
                """
                {
                    "title": "APIInfoObject",
                    "type": "object",
                    "properties": {
                        "version": {"type": "string"}
                    },
                    "required": ["version"]
                }
                """
            And the response json at $.version is equal to "1.0"
            