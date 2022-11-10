Feature: Step then the response header is eqaul to
    Validates the functionality of the step 
    "the response header <header> is eqaul to <value>"

    Background: We use a response double from where the JSON payload is retrieved.
        Given a test response
            And the response contains headers like
                """
                    {
                        "Content-Type": "application/json",
                        "Content-Length": "1700",
                        "Connection": "keep-alive",
                        "Date": "Thu, 10 Nov 2022 14:37:50 GMT",
                        "Access-Control-Allow-Origin": "*",
                        "Content-Encoding": "gzip"
                    }
                """

    Scenario: The retrieved value with the specified value
        Then the response header Content-Type is equal to application/json


    Scenario: Variables can be used in json path
        Then the response header ${CONTENT_LENGTH_HEADER} is equal to 1700


    Scenario: Variables can be used in expected value
        Then the response header Connection is equal to ${KEEP_ALIVE}
