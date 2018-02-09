################################################################################
Behave Restful
################################################################################

Behave Restful is a Behavior Driven Development (BDD) framework based on 
|behave|_, that implements a language suitable to test and validate REST APIs
and Services. It leverages the power of the |gherkin|_ language to write 
business readable tests that validate the behavior of REST APIs.

Although, Behave Restful is implemented in |python|_ and uses |behave|_ as 
underlying framework, it can test services implemented in any language as easy
as:

..  code-block:: gherkin

    Feature: API to add a new book to our collection
        As a user, I want to add a new book to my "to-read" collection.

        Scenario: Add a new book to collection.
            Given a request url http://my.reads/api/books
                And a request json payload
                    """
                    {
                        "category": "reference",
                        "author": "Nigel Rees",
                        "title": "Sayings of the Century",
                        "price": 8.95,
                        "status": "to-read"
                    }
                    """
            When the request sends POST
            Then the response status is CREATED
                And the response json matches
                    """
                    {
                        "title": "BookObject",
                        "type": "object"
                        "properties": {
                            "id": {"type": "number"},
                            "category": {"type": "string"},
                            "author": {"type": "string"},
                            "title": {"type": "string"},
                            "price": {"type": "number"},
                            "status": {"type": "string", "enum": ["to-read", "reading", "read"]}
                        },
                        "required": ["id", "category", "title"]
                    }
                    """
                And the response json at $.id is equal to 100
                And the response json at $.category is equal to "reference"
                And the response json at $.title is equal to "Sayings of the Century"


As you can see in the example, we send a POST request to the specified url with
a JSON payload, and we can validate the result very easy. First, we verify that
the status of the response is CREATED (it succeeds). Then we validate the
response JSON body using the expected |json_schema|_. Finally, we validate 
specific values in the response using |json_path|_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
