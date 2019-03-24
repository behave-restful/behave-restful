Feature: Sample Feature
    This is a sample feature that allows you to test that everything is working.
    You can remove it once you start adding your own features, or you can use it
    as a template for your projects.

    Scenario: We send a request to the Github API base url
        This scenario access the Github API base url to retrieve information
        about the service.

        Given a request url ${BASE_URL}
        When the request sends GET
        Then the response status is OK
            And the response json at $.current_user_url is equal to "${BASE_URL}/user"
