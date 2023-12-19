import pygame
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
    TextView,
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


class MockScreen:
    @staticmethod
    def fill(color):
        pass

    @staticmethod
    def blit(image, area):
        pass


class MockTimeAndClock:
    def __init__(self):
        self.current_time = 0

    def get_ticks(self):
        return self.current_time

    def tick(self, number):
        self.current_time += 1


@pytest.fixture
def mock_pygame(monkeypatch):
    """Disables pygame rendering for faster unit testing"""
    monkeypatch.setattr(pygame.display, "flip", lambda: None)

    def mock_render(self, message=None):
        pass

    monkeypatch.setattr(TextView, "render_message", mock_render)


@pytest.fixture
def game_state_before_end():
    game_state = game.GameState()
    game_state.stage = game.GameStage.PLAYING
    game_state.PLAYERS[0].hand = [Card(Rank.SEVEN, Suit.HEARTS)]
    game_state.PLAYERS[1].hand = [Card(Rank.SIX, Suit.HEARTS)]
    game_state.PLAYERS[2].hand = [Card(Rank.NINE, Suit.SPADES)]
    game_state.current_trick = {"cards": {}, "lead_player": 1, "winner": None}
    game_state.TRUMP_SUIT = Suit.CLUBS
    game_state.current_lead = 1
    game_state.next_to_play = 1
    return game_state


class MockOneEvent:
    def __init__(self):
        self.type = None
        self.pos = None


class MockLastTrickEvent:
    def __init__(self, click_pos=(0, 0)):
        self.turn = 0
        self.player_turn_order = [1, 2, 0, 0]
        self.click_pos = click_pos

    def get(self):
        this_turn_events = []
        if self.player_turn_order[self.turn] == 0:
            click_event = MockOneEvent
            click_event.type = pygame.MOUSEBUTTONUP
            click_event.pos = self.click_pos
            this_turn_events.append(click_event)
        self.turn += 1
        return this_turn_events

    def set_click_position(self, click_pos):
        self.click_pos = click_pos


def test_playing_loop_last_trick_ends_game(
    monkeypatch, mock_pygame, game_state_before_end
):
    human_hand = game_state_before_end.PLAYERS[0].hand
    mock_images_dict = {
        "hearts": {"seven": None, "six": None},
        "spades": {"nine": None},
    }
    clickable_human_hand = graphics.get_clickable_cards(human_hand, mock_images_dict)
    graphics.center_cards(clickable_human_hand)
    card_area = clickable_human_hand[0].clickable_area
    click_pos = card_area.centerx, card_area.centery
    event = MockLastTrickEvent(click_pos)
    monkeypatch.setattr(pygame, "event", event)
    mock_time = MockTimeAndClock()
    monkeypatch.setattr(pygame, "time", mock_time)
    # We set the milliseconds between plays to a negative value so
    # `get_ticks() > time_of_next_play` will always evaluate True
    monkeypatch.setattr(graphics, "MILLISECONDS_BETWEEN_PLAYS", -1)

    final_state = graphics.do_playing_loop(
        game_state_before_end,
        clickable_human_hand,
        mock_images_dict,
        MockScreen,
        mock_time,
        None,
        None,
    )
    assert len(final_state.PLAYERS[0].hand) == 0
    assert len(final_state.PLAYERS[1].hand) == 0
    assert len(final_state.PLAYERS[2].hand) == 0
