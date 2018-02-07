Feature: Step given a request url
    Validates the functionality of the given step "a request url"

    
    Scenario: Sets the specified url in the context
        Given a request url http://my.server.com/api/resource
        Then the context request url is equal to http://my.server.com/api/resource


    Scenario: Resolves variables in url
        Given a request url ${BASE_URL}/api/${RESOURCE}
        Then the context request url is equal to http://my.server.com/api/resource

