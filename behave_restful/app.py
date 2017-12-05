"""
Implements the Behave Restful application object which initializes the global
execution context providing access to directories and other services to 
simplify testing.  
"""
import os

class BehaveRestfulApp(object):
    """
    Behave Restful application class used to initialize the execution context
    for a test run.
    """

    def initialize_context(self, context, test_dir):
        """
        Initializes the provide context object exposing through it relevant
        directories and services. 

        :param context:
            A behave context object.
        :param test_dir:
            Directory where the tests are located. This is, usually, the 
            features folder of the test project.
        """
        context.test_dir = test_dir
        context.working_dir = os.getcwd()
    