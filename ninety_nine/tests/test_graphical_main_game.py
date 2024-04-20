import random
from dataclasses import dataclass
from unittest.mock import Mock

import pygame
import pytest
from ninety_nine import graphical_main_game as graphics
from ninety_nine import ninety_nine_state as game
from ninety_nine.monte_carlo_tree_search import NinetyNineMCST
from ninety_nine.ninety_nine_state import Card, Trick
from ninety_nine.constants import (
    Rank,
    Suit,
    PlayerTypes,
)
from ninety_nine.graphical_main_game import (
    ClickableCard,
    TextView,
    IMAGES_DIRECTORY_PATH,
    FULL_HAND_LEFT,
    HAND_TOP,
    SPACE_BETWEEN_CARDS,
    Button,
    AI_PLAYER_COMBINATION,
)


@pytest.mark.parametrize(
    "card,filename",
    [
        (Card(Rank.ACE, Suit.SPADES), "spades_ace.svg"),
        (Card(Rank.ACE, Suit.CLUBS), "clubs_ace.svg"),
    ],
)
def test_filename_from_ace_of_spades(card, filename):
    assert (
        graphics.get_image_filename_from_card(card)
        == f"{IMAGES_DIRECTORY_PATH}/{filename}"
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
    monkeypatch.setattr(graphics, "draw_button", lambda screen, button: None)

    def mock_render(self, message=None):
        pass

    monkeypatch.setattr(TextView, "render_message", mock_render)


@pytest.fixture
def game_state_before_end(request):
    game_state = game.GameState()
    game_state.stage = game.GameStage.PLAYING
    game_state.PLAYERS[0].hand = [Card(Rank.SEVEN, Suit.HEARTS)]
    game_state.PLAYERS[1].hand = [Card(Rank.SIX, Suit.HEARTS)]
    game_state.PLAYERS[2].hand = [Card(Rank.NINE, Suit.SPADES)]
    game_state.current_trick = Trick(
        {},
        request.param,
        None,
    )
    game_state.TRUMP_SUIT = Suit.CLUBS
    game_state.current_lead = request.param
    game_state.next_to_play = request.param
    return game_state


@pytest.fixture
def final_scores(request):
    return request.param


@pytest.fixture
def turn_order(request):
    return request.param


@dataclass
class MockOneEvent:
    type: int = None
    pos: tuple = None


class MockLastTrickEvent:
    def __init__(self, click_pos=(0, 0)):
        self.turn = 0
        self.player_turn_order = [1, 2, 0, "continue"]
        self.click_pos = click_pos
        self.continue_pos = (graphics.BUTTON_LEFT + 3, graphics.BUTTON_TOP + 3)

    def get(self):
        this_turn_events = []
        this_turn_event = self.player_turn_order[self.turn]
        if this_turn_event in (0, "continue"):
            click_event = MockOneEvent()
            click_event.type = pygame.MOUSEBUTTONUP
            if this_turn_event == 0:
                click_event.pos = self.click_pos
            elif this_turn_event == "continue":
                click_event.pos = self.continue_pos
            this_turn_events.append(click_event)
        self.turn += 1
        return this_turn_events

    def set_click_position(self, click_pos):
        self.click_pos = click_pos


@pytest.mark.parametrize(
    "game_state_before_end,final_scores,turn_order",
    [
        pytest.param(
            1, {0: 1, 1: 20, 2: 20}, [1, 2, 0, "continue"], id="player_1_leads"
        ),
        pytest.param(
            2, {0: 20, 1: 20, 2: 1}, [2, 0, 1, "continue"], id="player_2_leads"
        ),
        pytest.param(
            0, {0: 1, 1: 20, 2: 20}, [0, 1, 2, "continue"], id="human_player_leads"
        ),
    ],
    indirect=True,
)
def test_playing_loop_last_trick_ends_game(
    monkeypatch, mock_pygame, game_state_before_end, final_scores, turn_order
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
    event.player_turn_order = turn_order
    monkeypatch.setattr(pygame, "event", event)
    mock_screen = MockScreen()
    mock_time = MockTimeAndClock()
    monkeypatch.setattr(pygame, "time", mock_time)
    # We set the milliseconds between plays to a negative value so
    # `get_ticks() > time_of_next_play` will always evaluate True
    monkeypatch.setattr(graphics, "MILLISECONDS_BETWEEN_PLAYS", -1)

    final_state = graphics.do_playing_loop(
        game_state_before_end,
        clickable_human_hand,
        mock_images_dict,
        mock_screen,
        mock_time,
        None,
        None,
    )

    assert game.get_scores(final_state) == final_scores

    assert len(final_state.PLAYERS[0].hand) == 0
    assert len(final_state.PLAYERS[1].hand) == 0
    assert len(final_state.PLAYERS[2].hand) == 0


@pytest.fixture
def images_dict():
    return graphics.make_images_dict(game.get_all_cards())


@pytest.fixture
def all_tricks_plays():
    return [
        # ( PlayerNum, CardToPlay )
        (0, Card(Rank.ACE, Suit.SPADES)),
        (1, Card(Rank.KING, Suit.SPADES)),
        (2, Card(Rank.SEVEN, Suit.SPADES)),
        ("continue", None),
        (0, Card(Rank.SIX, Suit.CLUBS)),
        (1, Card(Rank.NINE, Suit.CLUBS)),
        (2, Card(Rank.KING, Suit.CLUBS)),
        ("continue", None),
        (2, Card(Rank.JACK, Suit.DIAMONDS)),
        (0, Card(Rank.EIGHT, Suit.DIAMONDS)),
        (1, Card(Rank.KING, Suit.DIAMONDS)),
        ("continue", None),
        (1, Card(Rank.SEVEN, Suit.CLUBS)),
        (2, Card(Rank.QUEEN, Suit.CLUBS)),
        (0, Card(Rank.ACE, Suit.CLUBS)),
        ("continue", None),
        (0, Card(Rank.ACE, Suit.DIAMONDS)),
        (1, Card(Rank.ACE, Suit.HEARTS)),
        (2, Card(Rank.SIX, Suit.DIAMONDS)),
        ("continue", None),
        (0, Card(Rank.QUEEN, Suit.HEARTS)),
        (1, Card(Rank.KING, Suit.HEARTS)),
        (2, Card(Rank.SIX, Suit.HEARTS)),
        ("continue", None),
        (1, Card(Rank.TEN, Suit.CLUBS)),
        (2, Card(Rank.JACK, Suit.CLUBS)),
        (0, Card(Rank.SIX, Suit.SPADES)),
        ("continue", None),
        (0, Card(Rank.QUEEN, Suit.SPADES)),
        (1, Card(Rank.JACK, Suit.HEARTS)),
        (2, Card(Rank.EIGHT, Suit.CLUBS)),
        ("continue", None),
        (0, Card(Rank.JACK, Suit.SPADES)),
        (1, Card(Rank.SEVEN, Suit.HEARTS)),
        (2, Card(Rank.TEN, Suit.HEARTS)),
        ("continue", None),
    ]


@pytest.fixture
def all_human_plays(all_tricks_plays):
    human_plays_only = [x[1] for x in all_tricks_plays if x[0] in (0, "continue")]
    clickable_human_plays = []
    for card in human_plays_only:
        if card is None:
            clickable_human_plays.append(None)
        else:
            clickable_human_plays.append(ClickableCard(card.rank, card.suit))
    return clickable_human_plays


@pytest.fixture
def all_random_plays(all_tricks_plays):
    return [x[1] for x in all_tricks_plays if x[0] in (1, 2)]


def test_human_list_filtering(all_human_plays):
    assert len(all_human_plays) == 18


def test_random_list_filtering(all_random_plays):
    assert len(all_random_plays) == 18


@pytest.fixture()
def click_continue_event():
    click_continue_event = MockOneEvent()
    click_continue_event.type = pygame.MOUSEBUTTONUP
    click_continue_event.pos = (
        graphics.BUTTON_LEFT + 2,
        graphics.BUTTON_TOP + 2,
    )
    return click_continue_event


@pytest.fixture
def all_events(all_tricks_plays, click_continue_event):
    all_events = []
    for play in all_tricks_plays:
        if play[0] == 0:
            click_card_event = MockOneEvent()
            click_card_event.type = pygame.MOUSEBUTTONUP
            click_card_event.pos = (0, 0)
            all_events.append([click_card_event])
        elif play[0] in (1, 2):
            all_events.append([])
        if play[0] == "continue":
            all_events.append([click_continue_event])
    return all_events


def test_click_event(mock_pygame):
    continue_button = Button()
    assert continue_button.rect.collidepoint(
        (graphics.BUTTON_LEFT + 2, graphics.BUTTON_TOP + 2)
    )


def test_events_fixture(all_events):
    assert len(all_events) == 27 + 9
    assert len([event_list for event_list in all_events if event_list == []]) == 18
    assert isinstance(all_events[0][0], MockOneEvent)
    assert all_events[0][0].type == pygame.MOUSEBUTTONUP
    assert all_events[0][0].pos == (0, 0)


@pytest.fixture
def human_card_from_click_mock(all_human_plays):
    mock = Mock()
    mock.side_effect = all_human_plays
    return mock


@pytest.fixture
def random_card_from_choice_mock(all_random_plays):
    mock = Mock()
    mock.side_effect = all_random_plays
    return mock


@pytest.fixture
def all_cards_event_mock(all_events):
    mock = Mock()
    mock.side_effect = all_events
    return mock


def test_cards_event_mock(all_cards_event_mock, all_events):
    first_event = all_cards_event_mock()[0]
    assert first_event.pos == (0, 0)
    all_returns = [[first_event]]
    while True:
        try:
            next_event = all_cards_event_mock()
            all_returns.append(next_event)
        except StopIteration:
            break
    assert len(all_returns) == 27 + 9
    assert all_returns == all_events


def test_playing_loop_all_cards_get_played(
    monkeypatch,
    mock_pygame,
    images_dict,
    game_state_after_dealing_spades_trump,
    all_cards_event_mock,
    human_card_from_click_mock,
    random_card_from_choice_mock,
    clickable_hand,
):
    monkeypatch.setattr(random, "choice", random_card_from_choice_mock)
    monkeypatch.setattr(graphics, "get_card_from_click", human_card_from_click_mock)
    monkeypatch.setattr(pygame.event, "get", all_cards_event_mock)
    mock_screen = MockScreen()
    mock_time = MockTimeAndClock()
    monkeypatch.setattr(pygame, "time", mock_time)
    # We set the milliseconds between plays to a negative value so
    # `get_ticks() > time_of_next_play` will always evaluate True
    monkeypatch.setattr(graphics, "MILLISECONDS_BETWEEN_PLAYS", -1)

    assert game_state_after_dealing_spades_trump.next_to_play == 0

    final_state = graphics.do_playing_loop(
        game_state_after_dealing_spades_trump,
        clickable_hand,
        images_dict,
        mock_screen,
        mock_time,
        None,
        None,
    )

    assert len(final_state.PLAYERS[1].hand) == 0


@pytest.fixture
def ai_versus_random_player_combination():
    AI_PLAYER_COMBINATION[0] = PlayerTypes.RANDOM
    return AI_PLAYER_COMBINATION


@pytest.fixture
def empty_events_with_continues_mock(click_continue_event):
    mock = Mock()
    num_hands = 9
    mock.side_effect = [[click_continue_event] if i % 4 == 3 else [] for i in range(num_hands*4)]
    return mock


@pytest.mark.skip(reason="slow test")
def test_playing_loop_with_mcst_versus_random(
    monkeypatch,
    mock_pygame,
    images_dict,
    game_state_after_dealing_spades_trump,
    empty_events_with_continues_mock,
    ai_versus_random_player_combination,
    clickable_hand,
):
    monkeypatch.setattr(pygame.event, "get", empty_events_with_continues_mock)
    mock_screen = MockScreen()
    mock_time = MockTimeAndClock()
    monkeypatch.setattr(pygame, "time", mock_time)
    # We set the milliseconds between plays to a negative value so
    # `get_ticks() > time_of_next_play` will always evaluate True
    monkeypatch.setattr(graphics, "MILLISECONDS_BETWEEN_PLAYS", -1)

    assert game_state_after_dealing_spades_trump.next_to_play == 0

    final_state = graphics.do_playing_loop(
        game_state_after_dealing_spades_trump,
        clickable_hand,
        images_dict,
        mock_screen,
        mock_time,
        None,
        None,
        player_types=ai_versus_random_player_combination,
        mcst=NinetyNineMCST(game_state_after_dealing_spades_trump),
    )

    assert len(final_state.PLAYERS[1].hand) == 0


def test_main_menu_continue():
    selected_option = graphics.get_clicked_menu_option()
    assert selected_option == "Main Game"
