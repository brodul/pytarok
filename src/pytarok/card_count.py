from typing import List

from pytarok.cards import Card


def count_original(cards: List[Card]) -> int:
    """This implements https://www.pagat.com/tarot/counting.html the original method"""
    # split cards into batches of 3
    batches = [cards[i : i + 3] for i in range(0, len(cards), 3)]
    # number of points for each batch
    batch_sums = [sum(map(lambda c: c.point_value - 1, cs)) + 1 for cs in batches]
    # sum up all batches points
    return sum(batch_sums)

    # TODO: does not handle batches of len 2 and 1


count = count_original
