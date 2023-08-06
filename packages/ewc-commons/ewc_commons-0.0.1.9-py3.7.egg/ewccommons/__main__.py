"""EWC Commons Library

A collection of common useful code library stuff & a showcase for learning.
Also showcase how to use the Sophie subpackage module.
"""
# Import the current library version number.
from .__init__ import __version__, _app_name_

# Import the typing library so variables can be type cast
from typing import List, Tuple, Any

# Import the sys for args
import sys

# Import the Sophie launcher system needed
from ewccommons.sophie import get_launcher
from ewccommons.sophie.usage import CLIUsageHandler
from ewccommons.sophie.launcher import wrapped_launch_handler, SophieLauncher

# Import the collection of available modules
from ewccommons import dice
from ewccommons import dicerolls
from ewccommons import carddeck

# Define some library & launch level variables
_short_options_: str = "hvq:"
_long_options_: List = [
    "help",
    "version",
    "dice",
    "dicerolls=",
    "carddeck",
    "enquiry=",
]


def launch_option_handler(
    opt: str,
    arg: str,
    opts: Tuple,
    args: Tuple,
) -> Tuple[Any, ...]:
    """
    Just handler the launch option
    """
    if opt == "--dice":
        # Run the dice main module function
        dice.check_output()
    elif opt == "--dicerolls":
        # Convert the value to lower, split on space
        # Add any unnamed arguments as potential included option values
        ds: List[str] = arg.lower().split() + list(args)
        # Supply the arguments to the dicerolls main function for handling
        dicerolls.rolls(*ds)
    elif opt == "--carddeck":
        # Run the carddeck main module function
        carddeck.spread_deck()


def help_text() -> str:
    """
    Generate the help text to display.

    TODO get this to read from a file???

    :return: The app help text multiline string.
    :rtype: str
    """
    return "\n".join(
        [
            "  -h --help (Show this help)",
            "  -v --version (Show library version)",
            "  --dice (Run the dice module)",
            "  --dicerolls Optional[d6 ...] (Run the dicerolls module)",
            "  --carddeck (Run the carddeck module)",
            "  -q <enquiry> (Make an enquiry)",
        ]
    )


def main(*args) -> None:
    # Define the variable types
    sophie: SophieLauncher
    usage: CLIUsageHandler
    # Create a new app launcher & usage instance
    sophie, usage = get_launcher(
        _usage=CLIUsageHandler,
        app_name=_app_name_,
        version=__version__,
        short_options=_short_options_,
        long_options=_long_options_,
        help_text=help_text,
    )
    # Configure the launch to use the supplied cli arguments
    sophie.config_launch(args)
    # Check if something went wrong getting a processor
    if sophie.has_error:
        # Display the usage help & GTFO
        sophie.show_usage_help()
        sys.exit(sophie.what_went_wrong())
    # Let's have a look at what we got
    print(
        "Let's have a look:",
        "#############",
        "Sophie",
        sophie,
        "Usage",
        usage,
        "#############",
        sep="\n",
    )
    # Define the usage & types of variables to be used in this scope
    enquiry: str
    handler_results: List[Tuple[Any, ...]]
    other: Tuple
    # enquiry, args = sophie.launch(cli_argument_handler)
    enquiry, handler_results, other = sophie.launch(
        wrapped_launch_handler(launch_option_handler)
    )
    print(enquiry, handler_results, other)
    # sophie.show_usage_help()


# Call the main library init function
main(*sys.argv[1:])
