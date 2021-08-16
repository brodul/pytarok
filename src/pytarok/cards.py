from dataclasses import dataclass, field
from typing import List
import random
from functools import partial

RED_RANKS = '4 3 2 1 J C Q K'.split()
BLACK_RANKS = '7 8 9 10 J C Q K'.split()
RED_SUITS = '♢ ♡'.split()
BLACK_SUITS = '♣ ♠'.split()


@dataclass
class SuitCard:
    rank: str
    suit: str
    color: str

def make_deck():
    return [SuitCard(r, s, "red") for s in RED_SUITS for r in RED_RANKS] + [SuitCard(r, s, "black") for s in BLACK_SUITS for r in BLACK_RANKS]

def make_shuffled_deck():
    # todo not random
    random.shuffle(deck:=make_deck())
    return deck


@dataclass
class Deck:  
    cards: List[SuitCard] = field(default_factory=make_shuffled_deck)

