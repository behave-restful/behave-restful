Feature: Step then the response json at is equal to
    Validates the functionality of the step "the response json at <path> is equal to <value>"


    Background: We use a response double from where the JSON payload is retrieved.
        Given a test response
            And the response contains a json body like
                """
                { 
                    "store": {
                        "book": [ 
                        { 
                            "category": "reference",
                            "author": "Nigel Rees",
                            "title": "Sayings of the Century",
                            "price": 8.95,
                            "edition": 2
                        },
                        { 
                            "category": "fiction",
                            "author": "Evelyn Waugh",
                            "title": "Sword of Honour",
                            "price": 12.99,
                            "edition": 6
                        },
                        { 
                            "category": "fiction",
                            "author": "Herman Melville",
                            "title": "Moby Dick",
                            "isbn": "0-553-21311-3",
                            "price": 8.99,
                            "edition": 5
                        },
                        { 
                            "category": "fiction",
                            "author": "J. R. R. Tolkien",
                            "title": "The Lord of the Rings",
                            "isbn": "0-395-19395-8",
                            "price": 22.99,
                            "edition": 1
                        }
                        ],
                        "bicycle": {
                        "color": "red",
                        "price": 19.95
                        }
                    }
                }
                """


    Scenario: Validates value of specific string property
        Notice the value is surrounded by quotes to indicate is a string.

        Then the response json at $.store.book[0].author is equal to "Nigel Rees"


    Scenario: Validates value of specific integer property
        Notice integer values are not surrounded by quotes.

        Then the response json at $.store.book[2].edition is equal to 5


    Scenario: Validates value of specific double property
        Notice double values are not surrounded by quotes.
        
        Then the response json at $.store.book[3].price is equal to 22.99


    Scenario: Validates all values in specified range
        Then the response json at $.store.book[1:4].category is equal to "fiction"


    Scenario: Variables can be used in json path
        Then the response json at ${TITLE_PATH} is equal to "The Lord of the Rings"
            And the response json at $.store.book[${BOOK_INDEX}].title is equal to "Sword of Honour"
            And the response json at $.store.book[2].${TITLE} is equal to "Moby Dick"


    Scenario: Variables can be used in expected value
        Then the response json at $.store.book[1:4].category is equal to "${CATEGORY_FICTION}"
