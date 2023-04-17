from pytarok.cards import (
    generate_roman_number,
    make_suit_deck,
    make_tarok_deck,
    make_special_deck,
    make_shuffled_deck,
)


class TestGenerateRomanNumber:
    def test_two(self):
        got = generate_roman_number(2)
        want = "II"

        assert got == want

    def test_four(self):
        got = generate_roman_number(4)
        want = "IV"

        assert got == want

    def test_twenty(self):
        got = generate_roman_number(20)
        want = "XX"

        assert got == want

    def test_all(self):
        got = " ".join(map(generate_roman_number, range(2, 21)))
        want = "II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX"
        assert got == want


class TestMakeSuitDeck:
    def test_number_cards(self):
        deck = make_suit_deck()
        got = len(deck)
        want = 32
        assert got == want


class TestTarokDeck:
    def test_number_cards(self):
        deck = make_tarok_deck()
        got = len(deck)
        want = 19
        assert got == want


class TestSpecialDeck:
    def test_number_cards(self):
        deck = make_special_deck()
        got = len(deck)
        want = 3
        assert got == want


class TestMakeShuffledDeck:
    def test_number_cards(self):
        deck = make_shuffled_deck()
        got = len(deck)
        want = 54
        assert got == want
