"""EWC Commons Card Deck

Create a card deck, a combination of numbered and face cards per suite.

Can be used/invoked as a module, why? because print is a valid debug tool!
"""
# Import the typing library so variables can be type cast
from typing import List, Optional, Tuple
from typing_extensions import TypeAlias

# Import the sys to get any argv used
import sys
import itertools
import random

# Import library stuff
from ewccommons import str_lower_list
from ewccommons.errors import not_what_i_wanted

_Card_: TypeAlias = Tuple[str, str]
"""Type Alias Definition

An individual card variable structure.
"""

_Deck_: TypeAlias = List[_Card_]
"""Type Alias Definition

A deck of cards collection list variable structure.
"""

_Hand_: TypeAlias = List[_Card_]
"""Type Alias Definition

A hand of cards collection subset list variable structure.
"""

STANDARD_DECK_SIZE: int = 52
"""Module Constant

Set the number of cards in a standard deck.
"""

STANDARD_SUITS: List[str] = ["Hearts", "Clubs", "Diamonds", "Spades"]
"""Module Constant

Set the card suits of a standard deck.
"""

STANDARD_FACE_CARDS: List[str] = [
    "J",  # Jack
    "Q",  # Queen
    "K",  # King
    "A",  # Ace
]
"""Module Constant

Set the picture face cards of a standard deck.
"""


def new_deck() -> _Deck_:
    """
    Create a new deck of cards.

    :return: A deck of cards collection list.
    :rtype: `ewccommons.carddeck._Deck_`
    """
    # Generate the list of numbers from 2 to 10 & add the picture cards
    ranks: List[_Card_] = [
        str(rank) for rank in list(range(2, 11)) + STANDARD_FACE_CARDS
    ]
    # Create a list of ranked cards combined with suite
    deck: _Deck_ = [card for card in itertools.product(STANDARD_SUITS, ranks)]
    return deck


def shuffle_deck(deck: _Deck_) -> _Deck_:
    """
    Generate a new shuffled verson of the card deck.

    :param deck: A deck of cards collection list to shuffle.
    :type deck: `ewccommons.carddeck._Deck_`
    :return: A shuffled deck of cards collection list.
    :rtype: `ewccommons.carddeck._Deck_`
    """
    # Copy the original so we don't mutate it
    _deck: _Deck_ = deck.copy()
    # Shuffle & return the copy of the deck
    random.shuffle(_deck)
    return _deck


def new_shuffled_deck() -> _Deck_:
    """
    Generate a new shuffled deck of cards.

    :return: A shuffled deck of cards collection list.
    :rtype: `ewccommons.carddeck._Deck_`
    """
    return shuffle_deck(deck=new_deck())


def draw_card(deck: _Deck_, cards: Optional[int] = 1) -> Tuple[_Hand_, _Deck_]:
    """
    Draw a number of cards from the top of the deck.

    :param deck: A deck of cards collection to draw cards from.
    :type deck: `ewccommons.carddeck._Deck_`
    :param cards: The number of cards to draw from the deck, defaults to 1.
    :type cards: Optional[int], optional
    :return: A tuple of cards drawn & cards remaining in the deck.
    :rtype: Tuple[`ewccommons.carddeck._Hand_`, `ewccommons.carddeck._Deck_`]
    :raises: ValueError For invalid cards type.
    :raises: ValueError If the cards is less than 0 or cards is greater than the deck.
    """
    # Verify the drawn number of cards can be satisfied, more than 1 less than deck
    if not isinstance(cards, int):
        raise not_what_i_wanted(
            "Invalid value supplied for cards argument.", int, cards
        )
    if cards < 0:
        raise ValueError(
            "Invalid number of cards to draw from the deck, must be a positive integer."
        )
    if cards > len(deck):
        raise ValueError("Insufficient number of cards to draw from the deck.")
    # Get a copy of the deck so we can leave the original unchanged
    deck_remaining: _Deck_ = deck.copy()
    drawn: _Hand_ = list()
    # draw the top x number of cards from the start of the deck list
    while len(drawn) < cards:
        # Pop the top card off the deck & append it to the hand
        drawn.append(deck_remaining.pop(0))
    return drawn, deck_remaining


def spread_deck(*args) -> None:
    """Debug/Test function

    Print out the card decks for inspection.
    """
    print("Args", *args, "Args", "New Shuffled Deck", sep="\n")
    deck = new_shuffled_deck()
    for idx, card in enumerate(deck):
        print(f"Card {idx+1} is {card[1]} of {card[0]}")
    drawn, deck_remaining = draw_card(deck, cards=5)
    print(
        f"Drawn Len : {len(drawn)}",
        f"Deck Remain Len : {len(deck_remaining)}",
        "Drawn Cards",
        drawn,
        "Remaining Deck",
        sep="\n",
    )
    for idx, card in enumerate(deck_remaining):
        print(f"Card {idx+1} is {card[1]} of {card[0]}")


def main() -> None:
    """Main function

    Run as a module and convert any CLI arguments to lowercase.
    """
    # Call the main function with any command line arguments after the module name
    spread_deck(*str_lower_list(sys.argv[1:]))


# Make sure the script is being called as a script & not being imported into
# another module file
if __name__ == "__main__":
    # Call the main function
    main()
