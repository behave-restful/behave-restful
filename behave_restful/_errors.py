"""
Contains exception base classes for Behave Restful.
"""

class BehaveRestfulException(Exception):
    """
    Base class for exceptions raised by behave_restful.
    """

    def __str__(self):
        return self.__repr__()


    def __repr__(self):
        return "BehaveResfulException('Unknown Error')"
