from typing import List

from pytarok.cards import Card, Deck


def chunks(lst: List, n: int):
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def split_deck(deck: Deck):
    return deck[:6], *chunks(deck[6:], 16)


def count_original(cards: List[Card]) -> int:
    """This implements https://www.pagat.com/tarot/counting.html the original method"""
    # split cards into batches of 3
    batches = chunks(cards, 3)
    # number of points for each batch
    batch_sums = [sum(map(lambda c: c.point_value - 1, cs)) + 1 for cs in batches]
    # sum up all batches points
    return sum(batch_sums)

    # TODO: does not handle batches of len 2 and 1


count = count_original
