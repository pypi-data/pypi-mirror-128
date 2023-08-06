"""EWC Commons Sophie Launch System

Add CLI launch argument processing to any script easily.
"""
# Import the typing library so variables can be type cast
from typing import Any, Callable, Optional, Tuple, List
from typing_extensions import TypeAlias

from ewccommons import generate_app_version_string
from ewccommons.typing_extensions import TnGn, CliArgHandled, CliArgHandler
from ewccommons.sophie.errors import SophieError
from ewccommons.sophie.usage import CLIUsage
from ewccommons.sophie.processors import SophieProcessor, CLArgsProcessor

import sys


_app_name_: str = "EWC Sophie Launcher"
_app_version_: str = "0.0.1"

LaunchOptionHandler: TypeAlias = Callable[
    [
        str,
        str,
        Tuple[str],
        Tuple[str],
    ],
    Tuple[Any, ...],
]
"""Type Alias Definition

Define the callable signature for processing a launch option.
"""


def wrapped_launch_handler(handler: LaunchOptionHandler) -> CliArgHandler:
    """Launch Handler Decorator

    Create a wrapper to handle the help & version display for launch.

    :param handler: A callable function to handle the individual CLI arguments used.
    :type handler: `ewccommons.sophie.launcher.LaunchOptionHandler`
    :return: A wrapped function to handle the extraction of launch arguments.
    :rtype: `ewccommons.typing_extensions.CliArgHandler`
    """

    def handler_wrapper(
        opts: Tuple,
        args: Tuple,
        show_usage_help: TnGn,
        show_version: TnGn,
    ) -> CliArgHandled:
        """Decorative Handler Function

        Handle the processing of the cli arguments.

        :param opts: A list of CLI argument options used.
        :type opts: Tuple
        :param args: A list of CLI argument options used.
        :type args: Tuple
        :param show_usage_help: A callable to display the app usage help text.
        :type show_usage_help: `ewccommons.typing_extensions.TnGn`
        :param show_version: A callable to display the app version.
        :type show_version: `ewccommons.typing_extensions.TnGn`
        :return: The handled launch result.
        :rtype: `ewccommons.typing_extensions.CliArgHandled`
        """
        enquiry: str = None
        handler_response: List[Tuple[Any, ...]] = list()
        opt: str
        arg: str
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                # Just show the usage help & halt
                show_version()
                show_usage_help()
                sys.exit()
            elif opt in ("-v", "--version"):
                # Just show the version & halt
                show_version()
                sys.exit()
            elif opt in ("-q", "--enquiry"):
                # Assign the enquiry value
                enquiry = arg
            else:
                # Add the wrapped launch handler result
                handler_response.append(handler(opt, arg, opts, args))
        # Return the handled launch result
        return enquiry, handler_response, args

    # Return the launch handler wrapped function
    return handler_wrapper


class LaunchProcessor(SophieProcessor):
    """
    Processor class to extract the CLI arguments used.
    """

    def __init__(
        self,
        handler: CliArgHandler,
        show_usage_help: TnGn,
        show_version: TnGn,
        arg_processor: CLArgsProcessor,
    ) -> None:
        """Initialize the launch processor

        Set the instance properties.

        :param handler: A function to handle the launch.
        :type handler: `ewccommons.typing_extensions.CliArgHandler`
        :param show_usage_help: A function to display the app usage help text.
        :type show_usage_help: `ewccommons.typing_extensions.TnGn`
        :param show_version: A function to display the app version text.
        :type show_version: `ewccommons.typing_extensions.TnGn`
        :param arg_processor: The cli argument processor to use.
        :type arg_processor: :class:`ewccommons.sophie.processors.CLArgsProcessor`
        """
        # Makes sure it's correctly instantiated
        # Use a dictionary of function references as the processing payload
        super().__init__(
            payload={
                "handler": handler,
                "show_usage_help": show_usage_help,
                "show_version": show_version,
            }
        )
        # Set the cli argument processor to get the runtime options used
        self.arg_processor: CLArgsProcessor = arg_processor

    def process(self):
        """Abstraction Implementation

        process the command line arguments & return the corresponding data.
        """
        # Get the runtime cli options used
        opts, args = self.arg_processor.processed_result
        # Process with the launch options
        self.processed(
            _result=self.processing_payload["handler"](
                opts,
                args,
                self.processing_payload["show_usage_help"],
                self.processing_payload["show_version"],
            )
        )


class SophieLauncher:
    """
    Define the main CLI script launcher.
    """

    def __init__(
        self,
        usage: CLIUsage,
        app_name: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        """Initialize the sophie launch mechanism

        Set the instance properties.

        :param usage: The app usage instance.
        :type usage: :class:`ewccommons.sophie.usage.CLIUsage`
        :param name: An optional app name, defaults to EWC Sophie's.
        :type name: Optional[str]
        :param version: An optional app version string, defaults to EWC Sophie's.
        :type version: Optional[str]
        """
        # Check if defaults need to be set
        if app_name is None:
            app_name = _app_name_
        if version is None:
            version = _app_version_
        self.launch_error: SophieError = None
        self.usage: CLIUsage = usage
        self.__app_name: str = app_name
        self.__version: str = version
        self.__configured: bool = False

    @property
    def has_error(self) -> bool:
        """Instance Property

        Check if the launcher encountered an error.

        :return: True if there has been a launch error.
        :rtype: bool
        """
        return self.launch_error is not None

    @property
    def app_name(self) -> str:
        """Instance Property

        Get the name of the app instance.

        :return: The app name string.
        :rtype: str
        """
        return self.__app_name

    @property
    def app_version(self) -> str:
        """Instance Property

        Get the app instance version.

        :return: The app version string.
        :rtype: str
        """
        return self.__version

    def show_usage_help(self) -> None:
        """
        Display the help text by constructing the app name with the usage help.
        """
        print(self.usage.help(), sep=" ")

    def show_version(self) -> None:
        """
        Display the version text by constructing the app name with the version.
        """
        print(self)

    def config_launch(self, argv):
        """
        Configure the launch process.

        :param argv: The cli argument values used.
        """
        # Create a CLI argument processor
        self.arg_processor: CLArgsProcessor = CLArgsProcessor(
            argv=argv, usage=self.usage
        )
        # Process the commandline argv for launch options
        self.arg_processor.process()
        # Check for processor errors
        if self.arg_processor.has_error:
            self.launch_error = self.arg_processor.error

    def launch(
        self,
        handler: CliArgHandler,
    ) -> CliArgHandled:
        """
        Launch the module/script.

        :param handler: A function to handle the launch.
        :type handler: `ewccommons.typing_extensions.CliArgHandler`
        :return: The handled launch process.
        :rtype: `ewccommons.typing_extensions.CliArgHandled`
        """
        # Create a new launch processor
        launch_processor: LaunchProcessor = LaunchProcessor(
            handler=handler,
            show_usage_help=self.show_usage_help,
            show_version=self.show_version,
            arg_processor=self.arg_processor,
        )
        launch_processor.process()
        return launch_processor.processed_result

    def what_went_wrong(self) -> str:
        """
        Determine what if anything went wrong.

        :return: A string containing any errors encountered.
        :rtype: str
        """
        if not self.has_error:
            return "Program executed within accepted parameters."
        return "\n".join([str(self), "ERROR:", str(self.launch_error)])

    def __str__(self) -> str:
        """
        Get the object as a human readable string.

        :return: An App name - Version - x multiline string.
        :rtype: str
        """
        return generate_app_version_string(self.app_name, self.app_version)
