import pytest
from ninety_nine import graphical_main_game as graphics
from ninety_nine import ninety_nine_state as game
from ninety_nine.ninety_nine_state import Card
from ninety_nine.constants import (
    Rank,
    Suit,
)
from ninety_nine.graphical_main_game import (
    ClickableCard,
    IMAGES_DIRECTORY_PATH,
    FULL_HAND_LEFT,
    HAND_TOP,
    SPACE_BETWEEN_CARDS,
)


def test_filename_from_ace_of_spades(ace_of_spades):
    assert (
        graphics.get_image_filename_from_card(ace_of_spades)
        == f"{IMAGES_DIRECTORY_PATH}/spades_ace.png"
    )


def test_filename_from_ace_of_clubs():
    assert (
        graphics.get_image_filename_from_card(Card(Rank.ACE, Suit.CLUBS))
        == f"{IMAGES_DIRECTORY_PATH}/clubs_ace.png"
    )


def test_get_ace_of_clubs_image():
    graphics.load_bordered_image_of_card(Card(Rank.ACE, Suit.CLUBS))


@pytest.fixture
def clickable_six_of_clubs():
    card = ClickableCard(Rank.SIX, Suit.CLUBS)
    card.set_left(FULL_HAND_LEFT + SPACE_BETWEEN_CARDS)
    card.set_top(HAND_TOP)
    return card


@pytest.fixture
def clickable_ace_of_clubs():
    card = ClickableCard(Rank.ACE, Suit.CLUBS)
    card.set_left(FULL_HAND_LEFT)
    card.set_top(HAND_TOP)
    return card


@pytest.fixture
def clickable_partial_bid(clickable_six_of_clubs, clickable_ace_of_clubs):
    return [clickable_six_of_clubs, clickable_ace_of_clubs]


def test_get_bid_value(clickable_partial_bid):
    assert game.bid_value(clickable_partial_bid) == 6


def test_make_images_dict(cards_subset):
    images_dict = graphics.make_images_dict(cards_subset)
    assert images_dict.keys() == {"hearts", "clubs"}
    assert images_dict["hearts"].keys() == {"ace", "king"}
    assert images_dict["clubs"].keys() == {"ace", "king"}


def test_make_clickable_cards_from_starting_hand(
    sorted_first_hand, clickable_hand, full_images_dict
):
    assert (
        graphics.get_clickable_cards(sorted_first_hand, full_images_dict)
        == clickable_hand
    )


def test_get_images_from_cards(cards_subset, full_images_dict):
    list_of_images = graphics.get_images_from_cards(cards_subset, full_images_dict)
    assert len(list_of_images) == 4


def test_player_clicks_on_first(clickable_hand, clickable_ace_of_clubs):
    assert (
        graphics.get_card_from_click([FULL_HAND_LEFT + 3, HAND_TOP + 3], clickable_hand)
        == clickable_ace_of_clubs
    )


def test_player_clicks_on_second(clickable_hand, clickable_six_of_clubs):
    assert (
        graphics.get_card_from_click(
            [FULL_HAND_LEFT + SPACE_BETWEEN_CARDS + 3, HAND_TOP + 3],
            clickable_hand,
        )
        == clickable_six_of_clubs
    )


def test_player_clicks_nothing(clickable_hand):
    assert graphics.get_card_from_click([10, 10], clickable_hand) is None
