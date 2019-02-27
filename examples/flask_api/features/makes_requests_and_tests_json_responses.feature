Feature: Makes requests and tests json responses

  behave-restful includes step definitions
  that enable your tests to make parameterized
  GET and POST requests and test assertions 
  about the structure and content of the responses.

Scenario: Send a GET request with params and test the json response
        Given a request url http://127.0.0.1:5000/hello
            And request parameters
                | param | value |
                | name  | Sally |
        When the request sends GET
        Then the response status is OK
            And the response json matches
                """
                {
                    "title": "HelloResponse",
                    "type": "object",
                    "properties": {
                        "greeting": {"type": "string"}
                    },
                    "required": ["greeting"]
                }
                """
            And the response json at $.greeting is equal to "hello, Sally!"
            

Scenario: Send a POST request with json and test the json response
        Given a request url http://127.0.0.1:5000/hello
            And a request json payload
                """
                {
                    "name": "John"
                }
                """"
        When the request sends POST
        Then the response status is OK
            And the response json matches
                """
                {
                    "title": "HelloResponse",
                    "type": "object",
                    "properties": {
                        "greeting": {"type": "string"}
                    },
                    "required": ["greeting"]
                }
                """
            And the response json at $.greeting is equal to "hello, John!"
            