from pytarok.card_handling import count_original, split_deck


class TestCountOriginal:
    def test_non_shuffled(self, non_shuffled_deck):
        got = count_original(non_shuffled_deck)
        want = 70

        assert got == want

    def test_shuffled(self, deck):
        got = count_original(deck)
        want = 70

        assert got == want


def test_split_deck(non_shuffled_deck):
    talon, hands = split_deck(non_shuffled_deck)
    # total number of cards
    assert sum((len(talon), *map(len, hands))) == 54
    assert 6 == len(talon)
    assert 3 == len(hands)
    for hand in hands:
        assert 16 == len(hand)
