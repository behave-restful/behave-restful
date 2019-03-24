Feature: Project Creation
    This suite verify the correct implementation of the br-init app to create a
    new Behave Restful Project.


    Scenario: Creates project in default features folder
        The application creates the project in a default features folder when
        no directory is specifies as parameter.

        Given br-init is run with no parameters
        When the application executes
        Then the project is created at features folder


    Scenario: Creates project in specified location
        The application creates the project at the location specifies as
        parameter.

        Given br-init is run with project_dir
        When the application executes
        Then the project is created at project_dir folder


    Scenario: An exception is raised if specified folder exists
        The user specifies a folder that already exists, in which case the
        application raises an exception as exits with an error code

        Given br-init is run with existent
        When the application executes
        Then an exception is raised