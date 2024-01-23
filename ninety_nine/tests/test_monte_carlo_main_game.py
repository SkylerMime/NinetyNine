import pytest
import random
import ninety_nine.ninety_nine_state as game

from ninety_nine import human_ai_main_game
from ninety_nine.constants import PlayerTypes


@pytest.fixture()
def seed_random():
    random.seed(100)


def test_seed(seed_random):
    assert random.randint(0, 1000) == 149


@pytest.mark.parametrize(
    "scores,made_bids,expected_dict_sum",
    [
        ({0: 21, 1: 5, 2: 23}, {0: 1, 1: 0, 2: 1}, {0: 22, 1: 5, 2: 24}),
        ({0: 3, 1: 5, 2: 1}, {0: 0, 1: 0, 2: 0}, {0: 3, 1: 5, 2: 1}),
    ],
)
def test_bid_mask(scores, made_bids, expected_dict_sum):
    bid_mask = {
        player_num: 1 if scores[player_num] > 9 else 0 for player_num in range(3)
    }
    assert bid_mask == made_bids
    dict_sum = {
        player_num: scores[player_num] + made_bids[player_num]
        for player_num in range(3)
    }
    assert dict_sum == expected_dict_sum


def test_list_logic():
    my_list = []
    if my_list:
        truth_value = True
    else:
        truth_value = False
    assert truth_value is False


@pytest.mark.usefixtures("seed_random")
def test_monte_carlo_beats_random(game_state_after_bidding):
    player_types = {
        0: PlayerTypes.MONTE_CARLO_AI,
        1: PlayerTypes.RANDOM,
        2: PlayerTypes.RANDOM,
    }
    final_state = human_ai_main_game.play_one_hand_of_ninety_nine(
        game_state_after_bidding, 9, player_types
    )
    final_scores = game.get_scores(final_state)
    assert final_scores[0] > final_scores[1]
    assert final_scores[0] > final_scores[2]
