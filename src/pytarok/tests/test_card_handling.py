from pytarok.card_handling import count_original


class TestCountOriginal:
    def test_non_shuffled(self, non_shuffled_deck):
        got = count_original(non_shuffled_deck)
        want = 70

        assert got == want

    def test_shuffled(self, deck):
        got = count_original(deck)
        want = 70

        assert got == want
