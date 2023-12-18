import pytest
import pygame
import sys
from ninety_nine import graphical_main_game as graphics
from ninety_nine.constants import (
    Suit,
)
from ninety_nine.graphical_main_game import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    TEXTVIEW_WIDTH,
    TEXTVIEW_HEIGHT,
    TEXTVIEW_TOP,
    TEXTVIEW_LEFT,
    TEXTVIEW_COLOR,
    TEXTVIEW_TEXT_COLOR,
)


@pytest.fixture(scope="module")
def pygame_instance():
    pygame.init()

    yield pygame

    pygame.quit()


@pytest.fixture
def clubs_trump_message(pygame_instance):
    message = graphics.TextView()
    message.rect = pygame.Rect
    message.rect = pygame.Rect(
        TEXTVIEW_LEFT, TEXTVIEW_TOP, TEXTVIEW_WIDTH, TEXTVIEW_HEIGHT
    )
    message.bg_color = TEXTVIEW_COLOR
    message.text_color = TEXTVIEW_TEXT_COLOR
    message.render_message(f"Trump Suit: {Suit.CLUBS.name.capitalize()}")
    return message


def test_playing_phase(
    game_state_with_two_card_trick,
    clickable_hand,
    full_images_dict,
    clubs_trump_message,
    pygame_instance,
):
    screen = pygame_instance.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    assert (
        graphics.do_playing_loop(
            game_state_with_two_card_trick,
            clickable_hand,
            full_images_dict,
            screen,
            pygame_instance.time.Clock(),
            None,
            None,
        )
        is not None
    )


def test_final_scores(game_state_two_players_made_bid, pygame_instance):
    screen = pygame_instance.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    graphics.display_final_scores(
        screen, game_state_two_players_made_bid, pygame_instance.time.Clock()
    )
