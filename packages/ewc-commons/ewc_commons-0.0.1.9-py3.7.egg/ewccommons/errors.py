"""EWC Commons Exceptions/Errors Extension

Definition of errors & exceptions.
"""
# Import the typing library so variables can be type cast
from typing import Any, Optional


def not_what_i_wanted(message: str, expected: Any, got: Any) -> ValueError:
    """
    Create a ValueError describing what was wanted vs what was used.

    :param message: A string message to prefix the error message with.
    :type message: str
    :param expected: The expected argument value type.
    :type expected: Any
    :param got: The actual variable used.
    :type got: Any
    :return: The generated value error ready to raise.
    :rtype: ValueError
    """
    _expected = type(expected)
    _got = type(got)
    return ValueError(f"{message}: Expected [{_expected}] Got [{_got}]")


class AError(Exception):
    """
    Define a general error with ability to hold context.
    """

    def __init__(self, message: str, ctx: Optional[Any] = None) -> None:
        """Initialize the error base

        Set the message and any supporting context.

        :param message: The error message string.
        :type message: str
        :param ctx: Additional error context.
        :type ctx: Optional[Any], optional
        """
        # Makes sure it's correctly instantiated
        super().__init__(message)
        # Set the additional context
        self.__ctx = ctx

    @property
    def context(self):
        """Instance Property

        Provide access to any asscoiated context for the error.

        :return: The associated exception/error context.
        :rtype: Any
        """
        return self.__ctx
