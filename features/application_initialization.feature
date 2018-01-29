Feature: Application Initialization
    This suite validates the proper initialization of the application and
    the global context.


    Scenario: The context is initialized with application directories
        Then the context exposes the working directory
            And the context exposes the test directory


    Scenario: The context is initialized with the specified definition
        Then the definition var BR_TESTING_STATUS has a value of running


    @tagged
    Scenario: Environment hooks are registered
        Then environment hooks are registered and invoked