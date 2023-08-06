"""EWC Commons Sophie Typing Extension

Definition of extended/complex variable types that extend the basic typing set.
"""
# Import the typing library so variables can be type cast
from typing import Any, Callable, Tuple
from typing_extensions import TypeAlias

CliArgHandled: TypeAlias = Tuple[Any, ...]
"""Type Alias Definition

Define the return type of the callback handler function.
"""

TnGn: TypeAlias = Callable[[], None]
"""Type Alias Definition

Define a Takes Nothing, Gives Nothing function signature.
"""

CliArgHandler: TypeAlias = Callable[[Tuple, Tuple, TnGn, TnGn], CliArgHandled]
"""Type Alias Definition

Define the callback handler function signature.
"""

DroneProcessorResult: TypeAlias = Tuple[Any, ...]
"""Type Alias Definition

Define the processed result variable type for DroneProcessors.
"""
