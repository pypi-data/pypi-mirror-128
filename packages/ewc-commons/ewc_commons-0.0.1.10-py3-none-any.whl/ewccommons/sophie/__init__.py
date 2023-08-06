"""EWC Commons Sophie

A framework for creating stuff.
"""
# Import the typing library so variables can be type cast
from typing import Optional, List, Tuple

from ewccommons.sophie.launcher import _app_name_, _app_version_, SophieLauncher
from ewccommons.sophie.usage import CLIUsageHandler


def get_launcher(
    _usage: CLIUsageHandler,
    app_name: Optional[str] = _app_name_,
    version: Optional[str] = _app_version_,
    short_options: Optional[str] = "hvq:",
    long_options: Optional[List] = ["help", "version", "enquiry="],
    help_text="-q <enquiry>",
) -> Tuple[SophieLauncher, CLIUsageHandler]:
    """Helper Function

    Shortcut method to create a SophieLauncher.

    :param _usage: The app usage class to use.
    :type _usage: :class:`ewccommons.sophie.usage.CLIUsage`
    :param app_name: An app name.
    :type name: Optional[str]
    :param version: An app version string.
    :type name: Optional[str]
    :param short_options: The string of 1 character cli options.
    :type short_options: Optional[str]
    :param long_options: The List of long cli options names.
    :type long_options: Optional[List[str]]
    :param help_text: The help text string or function to generate it.
    :type help_text: str, Callable[[], str]
    :return: The SophieLauncher and the CLIUsageHandler created to launch.
    :rtype: Tuple[SophieLauncher, CLIUsageHandler]
    """
    # TODO maybe add protection for the default param values as the can get fudged
    # Create the usage instance
    usage: CLIUsageHandler = _usage(
        short_options=short_options,
        long_options=long_options,
        help_text=help_text,
    )
    # Create the launcher with the usage
    sophie: SophieLauncher = SophieLauncher(
        usage=usage,
        app_name=app_name,
        version=version,
    )
    return sophie, usage
