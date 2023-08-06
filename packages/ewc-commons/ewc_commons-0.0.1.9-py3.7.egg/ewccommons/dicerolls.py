"""EWC Commons Dice Rolls

Create fixed instance versions of common sided Dice set.
Provides a convenient way of simulating random dice rolling.

Can be used/invoked as a module to generate dice roll values.
"""
# Import the sys to get any argv used
import sys

# Import library stuff & the Dice module to add some convenience
# objects & functions for dice rolling
from ewccommons import str_lower_list
from ewccommons.dice import Dice

D3: Dice = Dice(3, name="D3", val=None)
"""Module Object Instance

Create a D3 3 sided Dice instance with a random rolled start.
"""

D4: Dice = Dice(4, name="D4", val=None)
"""Module Object Instance

Create a D4 4 sided Dice instance with a random rolled start.
"""

D6: Dice = Dice(6, name="D6", val=None)
"""Module Object Instance

Create a D6 6 sided Dice instance with a random rolled start.
"""

D8: Dice = Dice(8, name="D8", val=None)
"""Module Object Instance

Create a D8 8 sided Dice instance with a random rolled start.
"""

D10: Dice = Dice(10, name="D10", val=None)
"""Module Object Instance

Create a D10 10 sided Dice instance with a random rolled start.
"""

D12: Dice = Dice(12, name="D12", val=None)
"""Module Object Instance

Create a D12 12 sided Dice instance with a random rolled start.
"""

D20: Dice = Dice(20, name="D20", val=None)
"""Module Object Instance

Create a D20 20 sided Dice instance with a random rolled start.
"""


def roll_d3() -> int:
    """
    Roll the D3 dice instance.

    :return: A randomly chosen integer between 1 and 3.
    :rtype: int
    """
    return D3.roll()


def roll_d4() -> int:
    """
    Roll the D4 dice instance.

    :return: A randomly chosen integer between 1 and 4.
    :rtype: int
    """
    return D4.roll()


def roll_d6() -> int:
    """
    Roll the D6 dice instance.

    :return: A randomly chosen integer between 1 and 6.
    :rtype: int
    """
    return D6.roll()


def roll_d8() -> int:
    """
    Roll the D8 dice instance.

    :return: A randomly chosen integer between 1 and 8.
    :rtype: int
    """
    return D8.roll()


def roll_d10() -> int:
    """
    Roll the D10 dice instance.

    :return: A randomly chosen integer between 1 and 10.
    :rtype: int
    """
    return D10.roll()


def roll_d12() -> int:
    """
    Roll the D12 dice instance.

    :return: A randomly chosen integer between 1 and 12.
    :rtype: int
    """
    return D12.roll()


def roll_d20() -> int:
    """
    Roll the D20 dice instance.

    :return: A randomly chosen integer between 1 and 20.
    :rtype: int
    """
    return D20.roll()


def roll_d100() -> int:
    """
    Simulate rolling a D100 the same way as table-top.
    Roll 2 D10 dice.

    :return: A randomly chosen integer between 1 and 100.
    :rtype: int
    """
    # Roll a ten sided die as the 10s die value
    # Removing 1 from the tens value allows the multiplier to work
    tens: int = D10.roll() - 1
    # Roll the units & return the sum
    units: int = D10.roll()
    # Return the modified tens to give us 00, 10...90 + the units (1 to 10)
    return (tens * 10) + units


def rolls(*args) -> None:
    """Debug/Test function

    Make dice rolls based on supplied arguments.
    """
    # Check for die rolls in the supplied arguments list
    # There is no reason why D10, D12 & D20 use the object & not the
    # `roll_d` function, other than to demonstrate
    print(args)
    if "d3" in args:
        print(f"{D3.name} Rolls...", roll_d3())
    if "d4" in args:
        print(f"{D4.name} Rolls...", roll_d4())
    if "d6" in args:
        print(f"{D6.name} Rolls...", roll_d6())
    if "d8" in args:
        print(f"{D8.name} Rolls...", roll_d8())
    if "d10" in args:
        print(f"{D10.name} Rolls...", D10.roll())
    if "d12" in args:
        print(f"{D12.name} Rolls...", D12.roll())
    if "d20" in args:
        print(f"{D20.name} Rolls...", D20.roll())
    if "d100" in args:
        print("D100 Rolls...", roll_d100())


def main() -> None:
    """Main function

    Run as a module and convert any CLI arguments to lowercase.
    """
    # Call the main function with any command line arguments after the module name
    rolls(*str_lower_list(sys.argv[1:]))


# Make sure the script is being called as a script & not being imported into
# another module file
if __name__ == "__main__":
    # Call the main function
    main()
