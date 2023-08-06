"""EWC Commons Sophie Exceptions/Errors Extension

Definition of Sophie related errors & exceptions.
"""
# Import the base exception error
from ewccommons.errors import AError


class SophieError(AError):
    """
    Define a general Sophie error with ability to hold context.
    """


class SophieExecutionError(AError):
    """
    Define a general Sophie execution error.
    """
