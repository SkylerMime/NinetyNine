import pytest
import builtins
import random
from ninety_nine import human_ai_main_game as main


def test_card_to_string(ten_of_hearts_string, ten_of_hearts):
    assert main.get_valid_card(ten_of_hearts_string) == ten_of_hearts


def test_get_human_bid(monkeypatch, player_before_bidding, bid, human_bid_mock):
    with monkeypatch.context() as m:
        m.setattr(builtins, "input", human_bid_mock)
        main.get_human_bid(player_before_bidding)
        assert player_before_bidding.bid == bid


def test_get_random_bid(monkeypatch, player_before_bidding, bid, random_bid_mock):
    monkeypatch.setattr(random, "choice", random_bid_mock)
    main.get_random_bid(player_before_bidding)
    assert player_before_bidding.bid == bid


def test_all_cards_played(game_state_after_dealing):
    for player in game_state_after_dealing.PLAYERS.values():
        player.hand = set()
    assert main.all_cards_played(game_state_after_dealing.PLAYERS) is True


def test_human_card_valid(monkeypatch, game_state_after_dealing, ace_of_spades):
    with monkeypatch.context() as m:
        m.setattr(builtins, "input", lambda: "AS")
        assert main.get_human_card_play(0, game_state_after_dealing) == ace_of_spades


def test_human_card_first_invalid(
    monkeypatch, two_human_plays_mock, game_state_after_dealing, ace_of_spades
):
    with monkeypatch.context() as m:
        m.setattr(builtins, "input", two_human_plays_mock)
        assert main.get_human_card_play(0, game_state_after_dealing) == ace_of_spades


def test_game_loop_all_cards_get_played(
    monkeypatch,
    human_plays_mock,
    both_random_plays_mock,
    game_state_after_dealing_spades_trump,
):
    monkeypatch.setattr(random, "choice", both_random_plays_mock)
    with monkeypatch.context() as m:
        m.setattr(builtins, "input", human_plays_mock)
        final_state = main.play_one_hand_of_ninety_nine(game_state_after_dealing_spades_trump)
        assert len(final_state.PLAYERS[0].hand) == 0
        assert len(final_state.PLAYERS[1].hand) == 0
        assert len(final_state.PLAYERS[2].hand) == 0


def test_order_cards_by_suit_and_rank(hand_after_playing, sorted_cards):
    assert main.get_sorted_cards(hand_after_playing) == sorted_cards
