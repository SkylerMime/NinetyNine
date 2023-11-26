import pytest
import pygame
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
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    HAND_X_POSITION,
    HAND_Y_POSITION,
    SPACE_BETWEEN_CARDS,
)


@pytest.fixture
def clickable_hand(sorted_cards):
    hand = []
    for card_num in range(len(sorted_cards)):
        card = sorted_cards[card_num]
        clickable_card = ClickableCard(card.rank, card.suit)
        clickable_card.card_image = graphics.load_bordered_image_of_card(clickable_card)
        clickable_card.set_left(HAND_X_POSITION + card_num * SPACE_BETWEEN_CARDS)
        hand.append(clickable_card)
    return hand


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
def full_images_dict():
    return graphics.make_images_dict(game.get_all_cards())


@pytest.fixture
def clickable_nine_of_clubs():
    card = ClickableCard(Rank.NINE, Suit.CLUBS)
    card.set_left(HAND_X_POSITION)
    card.set_top(HAND_Y_POSITION)
    return card


@pytest.fixture
def clickable_eight_of_clubs():
    card = ClickableCard(Rank.EIGHT, Suit.CLUBS)
    card.set_left(HAND_X_POSITION + SPACE_BETWEEN_CARDS)
    card.set_top(HAND_Y_POSITION)
    return card


def test_make_images_dict(cards_subset):
    images_dict = graphics.make_images_dict(cards_subset)
    assert images_dict.keys() == {"hearts", "clubs"}
    assert images_dict["hearts"].keys() == {"ace", "king"}
    assert images_dict["clubs"].keys() == {"ace", "king"}


def test_make_clickable_cards_from_starting_hand(
    sorted_cards, clickable_hand, full_images_dict
):
    assert (
        graphics.get_clickable_cards(sorted_cards, full_images_dict) == clickable_hand
    )


def test_get_images_from_cards(cards_subset, full_images_dict):
    list_of_images = graphics.get_images_from_cards(cards_subset, full_images_dict)
    assert len(list_of_images) == 4


def test_player_clicks_on_first(clickable_hand, clickable_nine_of_clubs):
    assert (
        graphics.get_card_from_click(
            [HAND_X_POSITION + 3, HAND_Y_POSITION + 3], clickable_hand
        )
        == clickable_nine_of_clubs
    )


def test_player_clicks_on_second(clickable_hand, clickable_eight_of_clubs):
    assert (
        graphics.get_card_from_click(
            [HAND_X_POSITION + SPACE_BETWEEN_CARDS + 3, HAND_Y_POSITION + 3],
            clickable_hand,
        )
        == clickable_eight_of_clubs
    )


def test_player_clicks_nothing(clickable_hand):
    assert (
        graphics.get_card_from_click([10, 10], clickable_hand) is None
    )
