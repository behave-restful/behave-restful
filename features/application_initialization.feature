Feature: Application Initialization
    This suite validates the proper initialization of the application and
    the global context.


    Scenario: The context is initialized with application directories
        Then the context exposes the working directory
            And the context exposes the test directory