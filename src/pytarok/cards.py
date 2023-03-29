import random
from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, Union


def generate_roman_number(rank: int) -> str:
    map_ = ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))
    accu = ""
    for i, rep in map_:
        accu += (rank // i) * rep
        rank = rank % i

    return accu


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
    view: str
    rank: int
    point_value: int = 1


# Skis, Mond and Pagat
@dataclass
class SpecialCard:
    view: str
    alt_view: str
    rank: int
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
RED_RANKS = (RTC("4"), RTC("3"), RTC("2"), RTC("1")) + FAMILY_RANKS
BLACK_RANKS = "7 8 9 10 J C Q K".split()

RED_SUITS = "♢ ♡".split()
BLACK_SUITS = "♣ ♠".split()


def make_suit_deck() -> List[SuitCard]:
    return [SuitCard(r, s, "red") for s in RED_SUITS for r in RED_RANKS] + [
        SuitCard(r, s, "black") for s in BLACK_SUITS for r in BLACK_RANKS
    ]


def make_tarok_deck() -> List[TArokCard]:
    return TarokCard


def make_shuffled_deck():
    # TODO: not random
    deck = make_suit_deck() + make_tarok_deck() + make_special_deck()
    random.shuffle(deck)
    return deck


@dataclass
class Deck:
    cards: List[SuitCard] = field(default_factory=make_shuffled_deck)


Card = Union[SuitCard, TarokCard, SpecialCard]
