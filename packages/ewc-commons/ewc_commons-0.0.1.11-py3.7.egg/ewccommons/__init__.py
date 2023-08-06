"""EWC Commons Library

A collection of common useful code library stuff & a showcase for learning.
"""
# Import the current library version number.
from .__version__ import __version__
from .typing_extensions import DroneProcessorResult
from .errors import AError

# Import the typing library so variables can be type cast
from typing import List, Optional, Any

# Import the use of abstract classes
from abc import ABC, abstractmethod

_app_name_: str = "EWC Commons Library"
"""
Define the application/module name.
"""


def generate_app_version_string(
    name: Optional[str] = None, version: Optional[str] = None
) -> str:
    """Helper Function

    Generates an App name - Version - x string.

    :param name: An app name, defaults to 'EWC Commons Library'.
    :type name: Optional[str], optional
    :param version: An app version, defaults to current library version.
    :type version: Optional[str], optional
    :return: The App name - Version - x multiline string.
    :rtype: str The app version string.
    """
    if name is None or not str(name):
        name = _app_name_
    if version is None or not version:
        version = __version__
    return "\n".join([str(name), f"Version - {version}"])


def str_lower_list(source_list: List[str]) -> List[str]:
    """Helper Function

    Convert a list of strings to lower case

    :param source_list: The source list of strings to convert to lower case.
    :type source_list: List[str]
    :return: The source list elements converted to lower case.
    :rtype: List[str]
    """
    return [str(_).lower() for _ in source_list]


class DroneProcessor(ABC):
    """Abstract Base Class

    Define the object signature of a processor.
    """

    @abstractmethod
    def __init__(self, payload: Any) -> None:
        """Initialize the abstract processor base

        Set the instance properties.

        :param payload: The payload to process.
        :type payload: Any
        """
        super().__init__()
        self.__processed: DroneProcessorResult = None
        self.__error: AError = None
        self.__process_payload: Any = payload

    @abstractmethod
    def process(self):
        """Abstraction Implementation

        Pro-cessing...
        """

    @property
    def exception_wrapper(self) -> AError:
        """Instance Property

        Provide a way of changing the exception wrapper used to return

        :return: The exception callable to wrap the encountered error.
        :rtype: :class:`ewccommons.errors.AError`
        """
        return AError

    @property
    def processing_payload(self) -> Any:
        """Instance Property

        Provide access to the processing payload.

        :return: The processing payload.
        :rtype: Any
        """
        return self.__process_payload

    @property
    def processed_result(self) -> DroneProcessorResult:
        """Instance Property

        Provide access to the processed payload result.

        :return: The processed payload.
        :rtype: `ewccommons.typing_extensions.DroneProcessorResult`
        """
        return self.__processed

    @property
    def has_error(self) -> bool:
        """Instance Property

        Check if the processor encountered an error.

        :return: True if an error has been encountered.
        :rtype: bool
        """
        return self.__error is not None

    @property
    def error(self) -> AError:
        """Instance Property

        Provide access to any Exceptions raised & intercepted.

        :return: The error that has been encountered is any.
        :rtype: :class:`ewccommons.errors.AError`
        """
        return self.__error

    def processed(self, _result: DroneProcessorResult) -> None:
        """
        Set processed payload result.

        :param _result: A tuple list of any processing results.
        :type _result: `ewccommons.typing_extensions.DroneProcessorResult`
        """
        self.__processed = _result

    def errored(self, _err: Exception) -> None:
        """
        Set awrapped encountered error / exception.

        :param _err: The error/exception intercepted.
        :type _err: :class:`Exception`
        """
        # Wrap the intercepted exception/error in a sophie error
        self.__error = self.exception_wrapper(str(_err), _err)
