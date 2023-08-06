"""EWC Commons Sophie Usage

Add CLI launch argument processing to any script easily.
"""
# Import the typing library so variables can be type cast
from typing import List, Callable

# Import the use of abstract classes
from abc import ABC, abstractmethod

from ewccommons import DroneProcessor


class CLIUsage(ABC):
    """Abstract Base Class

    Define how a CLI Usage handler should look.
    """

    default_short_options: str = "hv"
    """Class Property

    String list of 1 character default options for help & version
    """

    default_long_options: List[str] = ["help", "version"]
    """Class Property

    List of default long options names for help & version
    """

    @abstractmethod
    def __init__(self, short_options: str, long_options: List[str]) -> None:
        """Initialize the abstract usage base

        Set the usage details.

        :param short_options: The string list of 1 character cli options.
        :type short_options: str
        :param long_options: The List of long cli options names.
        :type short_options: List[str]
        """
        self.__short_options: str = short_options
        self.__long_options: List[str] = long_options
        self.arg_processor: DroneProcessor = None
        # Initialise the list of CLI arguments used at runtime
        self.__used: List[str] = list()
        self.__ignored_used: List[str] = list()

    @abstractmethod
    def help(self) -> str:
        """Abstraction Implementation

        Get the command line usage help.

        :return: The usage help text.
        :rtype: str
        """

    @property
    def short_options(self) -> str:
        """Instance Property

        Get all the cli 1 character options available.

        :return: The string list of 1 character cli options.
        :rtype: str
        """
        return self.__short_options

    @property
    def long_options(self) -> List[str]:
        """Instance Property

        Get a list of all the cli long options available.

        :return: The List of long cli options names.
        :rtype: List[str]
        """
        return self.__long_options

    @property
    def used(self) -> List[str]:
        """Instance Property

        Get a list of all the cli arguments used at runtime.

        :return: The list of all the runtime used cli options.
        :rtype: List[str]
        """
        return self.__used

    @property
    def ignored(self) -> List[str]:
        """Instance Property

        Get a list of any invalid cli arguments used at runtime.

        :return: The list of all the invalid/ignored runtime cli options used.
        :rtype: List[str]
        """
        return self.__ignored_used

    def using(self, arg_processor: DroneProcessor) -> None:
        """
        Provide a means of setting the CLI argument processor.

        :param arg_processor: Specify a argument processor to use.
        :type arg_processor: :class:`ewccommons.DroneProcessor`
        """
        self.arg_processor = arg_processor


class CLIUsageHandler(CLIUsage):
    """
    Create a CLI argument usage handler.
    """

    def __init__(self, short_options: str, long_options: List[str], help_text) -> None:
        """Initialize the cli usage

        Set the usage details.

        :param short_options: The string list of 1 character cli options.
        :type short_options: str
        :param long_options: The List of long cli options names.
        :type short_options: List[str]
        :param help_text: Help text string or function that generates it.
        :type help_text: str, Callable[[], str]
        """
        # Makes sure it's correctly instantiated
        super().__init__(short_options=short_options, long_options=long_options)
        # If the help text specified is not a callable function, wrap it in a lambda
        self._help_text: Callable[[], str] = (
            help_text if callable(help_text) else lambda: str(help_text)
        )

    def help(self) -> str:
        """Abstraction Implementation

        Get the usage help for the options.

        :return: The help text string.
        :rtype: str
        """
        return self._help_text()

    def __str__(self) -> str:
        """
        Get the object as a human readable string.

        :return: The usage help text string.
        :rtype: str
        """
        return "\n".join([self._help_text()])
