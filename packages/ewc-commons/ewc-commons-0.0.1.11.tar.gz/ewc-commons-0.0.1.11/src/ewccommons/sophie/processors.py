"""EWC Commons Sophie Processors

Collection of specific drone processors.
"""
# Import the get options to process command line arguments
import getopt

from ewccommons import DroneProcessor
from ewccommons.sophie.errors import SophieExecutionError
from ewccommons.sophie.usage import CLIUsage


class SophieProcessor(DroneProcessor):
    """
    Define the object signature of a processor.
    """

    @property
    def exception_wrapper(self) -> SophieExecutionError:
        """Instance Property

        Provide a way of changing the exception wrapper used to return

        :return: The exception callable to wrap the encountered error.
        :rtype: :class:`ewccommons.sophie.errors.SophieExecutionError`
        """
        return SophieExecutionError


class CLArgsProcessor(SophieProcessor):
    """
    Processor class to extract the CLI arguments used.
    """

    def __init__(self, argv, usage: CLIUsage) -> None:
        """Initialize the cli argument processor

        Set the instance properties

        :param argv: The cli argument values list.
        :type argv: Any
        :param usage: The cli usage instance to process for.
        :type usage: :class:`ewccommons.sophie.usage.CLIUsage`
        """
        # Makes sure it's correctly instantiated
        # Just use the argv as the payload
        super().__init__(payload=argv)
        self.usage: CLIUsage = usage

    def process(self):
        """Abstraction Implementation

        process the command line arguments & return the corresponding data.

        TODO make sure only valid argv values are used or it raises GetoptError.
        TODO Get the processed values exposed correctly.

        BUG Any unspecified --args options used in the supplied argv cause
            GetoptError(_('option --%s not recognized') % opt, opt)
            Which abondons the whole attempt, do not pass Go, do not collect $200.
        """
        try:
            # Extract the options & arguments specified from the supplied arguments
            opts, args = getopt.getopt(
                self.processing_payload,
                self.usage.short_options,
                self.usage.long_options,
            )
        except getopt.GetoptError as _err:
            # Hello there
            return self.errored(_err)
        # Set the options & arguments to process later
        # TODO Get the values exposed correctly
        self.processed(_result=(opts, args))
