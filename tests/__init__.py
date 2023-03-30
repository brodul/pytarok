import pytest

from pytarok.cards import make_deck


@pytest.fixture
def non_shuffled_deck():
    return make_deck()
