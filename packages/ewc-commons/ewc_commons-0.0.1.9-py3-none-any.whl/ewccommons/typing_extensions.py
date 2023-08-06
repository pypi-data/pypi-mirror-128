"""EWC Commons Sophie Typing Extension

Definition of extended/complex variable types that extend the basic typing set.
"""
# Import the typing library so variables can be type cast
from typing import Any, Callable, Tuple

_CLI_Arg_Handled_ = Tuple[Any, ...]
"""Type Alias Definition

Define the return type of the callback handler function.
"""

_TNGN_ = Callable[[], None]
"""Type Alias Definition

Define a Takes Nothing, Gives Nothing function signature.
"""

_CLI_Arg_Handler_ = Callable[[Tuple, Tuple, _TNGN_, _TNGN_], _CLI_Arg_Handled_]
"""Type Alias Definition

Define the callback handler function signature.
"""

_DroneProcessorResult_ = Tuple[Any, ...]
"""Type Alias Definition

Define the processed result variable type for DroneProcessors.
"""
