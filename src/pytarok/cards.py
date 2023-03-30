import random
from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, Tuple, Union, NewType


def generate_roman_number(rank: int) -> str:
    map_ = ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))
    accu = ""
    for i, rep in map_:
        accu += (rank // i) * rep
        rank = rank % i

    return accu


Suit = namedtuple("Suit", "suit_name suit_symbol")


BlackSuits = NewType("BlackSuit", Tuple[Suit])
RedSuits = NewType("RedSuit", Tuple[Suit])


@dataclass
class SuitCard:
    rank_short_name: str
    rank_name: str
    rank_weight: int
    suit_name: str
    suit_symbol: str
    color: str
    point_value: int


@dataclass
class TarokCard:
    rank_roman: str
    rank_weight: int
    point_value: int = 1


# Skis, Mond and Pagat
@dataclass
class SpecialCard:
    rank_roman: str
    rank_name: str
    rank_weigh: int
    point_value: int = 5


Card = Union[SuitCard, TarokCard, SpecialCard]

RankCardTemplate = RCT = namedtuple(
    "RankCardTemplate", ("rank_short_name", "rank_name", "rank_weight", "point_value")
)
FAMILY_RANKS = (
    RCT("J", "Jack", 5, 2),
    RCT("C", "Knight", 6, 3),
    RCT("Q", "Queen", 7, 4),
    RCT("K", "King", 8, 5),
)
RED_RANKS = (
    RCT("4", "Four", 1, 1),
    RCT("3", "Three", 2, 1),
    RCT("2", "Two", 3, 1),
    RCT("1", "One", 4, 1),
) + FAMILY_RANKS
BLACK_RANKS = (
    RCT("7", "Seven", 1, 1),
    RCT("8", "Eight", 2, 1),
    RCT("9", "Nine", 3, 1),
    RCT("10", "Ten", 4, 1),
) + FAMILY_RANKS

RED_SUITS = RedSuits(
    (
        Suit("Diamond", "♢"),
        Suit("Heart", "♡"),
    )
)
BLACK_SUITS = BlackSuits(
    (
        Suit("Club", "♣"),
        Suit("Spade", "♠"),
    )
)

Card = Union[SuitCard, TarokCard, SpecialCard]
Deck = List[Card]


def make_suit_deck() -> List[SuitCard]:
    return [SuitCard(*s, "red", *r) for s in RED_SUITS for r in RED_RANKS] + [
        SuitCard(*s, "black", *r) for s in BLACK_SUITS for r in BLACK_RANKS
    ]


def make_tarok_deck() -> List[TarokCard]:
    return [TarokCard(generate_roman_number(i), i) for i in range(2, 21)]


def make_special_deck() -> List[SpecialCard]:
    return [
        SpecialCard(*args)
        for args in (("I", "Pagat", 1), ("XXI", "Mond", 21), ("S", "Skis", 22))
    ]


def shuffle(deck: Deck, seed=None) -> Deck:
    deck_copy = deck[:]
    # Relatively random
    for i in range(3):
        random.seed(seed)
        random.shuffle(deck_copy)

    return deck_copy


def make_deck():
    deck = make_suit_deck() + make_tarok_deck() + make_special_deck()
    return deck


def make_shuffled_deck(seed=None):
    deck = make_deck()
    deck = shuffle(deck, seed)
    return deck
