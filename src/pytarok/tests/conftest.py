import pytest

from pytarok.cards import make_deck, make_shuffled_deck


@pytest.fixture
def non_shuffled_deck():
    return make_deck()


@pytest.fixture(scope="module", params=["seed1", "seed2"])
def deck(request):
    return make_shuffled_deck(request.param)
