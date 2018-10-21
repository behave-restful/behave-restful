Feature: Step then the response json at is not null
    Validates the functionality of the step 
    "the response json at <path> is not null"

    Background: We use a response double from where the JSON payload is retrieved.
        Given a test response
            And the response contains a json body like
                """
                { 
                    "songs": [
                        {
                            "title": "Green Onions",
                            "link": "http://music.service/1",
                            "available": true
                        },
                        {
                            "title": "Storm Monday",
                            "link": "http://music.service/2",
                            "available": true
                        },
                        {
                            "title": "Rock This House",
                            "link": null,
                            "available": false
                        },
                        {
                            "title": "La grange",
                            "link": null,
                            "available": false
                        }
                    ]
                }
                """
    
    Scenario: The retrieved value is not null
        Then the response json at $.songs[0].link is not null


    Scenario: Validates all values in a specified range
        Then the response json at $.songs[0:2].link is not null


    Scenario: Variables can be used in json path
        Then the response json at ${LINK_PATH} is not null

