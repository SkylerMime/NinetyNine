import pytest
from ninety_nine import graphical_main_game as graphics
from unittest.mock import Mock
import ninety_nine.human_ai_main_game as game_display
from ninety_nine import ninety_nine_state as game
from ninety_nine.ninety_nine_state import Card
from ninety_nine.constants import Rank, Suit
from ninety_nine.graphical_main_game import (
    ClickableCard,
    FULL_HAND_LEFT,
    SPACE_BETWEEN_CARDS,
)


ARBITRARY_SEED = 5


@pytest.fixture
def full_images_dict():
    return graphics.make_images_dict(game.get_all_cards())


@pytest.fixture
def clickable_hand(sorted_first_hand):
    hand = []
    for card_num in range(len(sorted_first_hand)):
        card = sorted_first_hand[card_num]
        clickable_card = ClickableCard(card.rank, card.suit)
        clickable_card.card_image = graphics.load_bordered_image_of_card(clickable_card)
        clickable_card.set_left(FULL_HAND_LEFT + card_num * SPACE_BETWEEN_CARDS)
        hand.append(clickable_card)
    return hand


@pytest.fixture
def bid():
    return {
        game.Card(Rank.ACE, Suit.SPADES),
        game.Card(Rank.KING, Suit.SPADES),
        game.Card(Rank.QUEEN, Suit.SPADES),
    }


@pytest.fixture
def ranks_subset():
    return {Rank.ACE, Rank.KING}


@pytest.fixture
def suits_subset():
    return {Suit.HEARTS, Suit.CLUBS}


@pytest.fixture
def cards_subset():
    return {
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.CLUBS),
    }


@pytest.fixture
def human_bid_mock():
    mock = Mock()
    mock.side_effect = ["AS", "KS", "QS"]
    return mock


@pytest.fixture
def random_bid_mock():
    mock = Mock()
    mock.side_effect = [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.SPADES),
    ]
    return mock


@pytest.fixture
def human_plays_mock():
    mock = Mock()
    mock.side_effect = [
        "AS",
        "6C",
        "8D",
        "AC",
        "AD",
        "QH",
        "6S",  # ASSUMPTION: Spades is trump suit
        "QS",
        "JS",
    ]
    return mock


@pytest.fixture
def two_human_plays_mock():
    mock = Mock()
    mock.side_effect = ["KH", "AS"]
    return mock


@pytest.fixture
def both_random_plays_mock():
    mock = Mock()
    mock.side_effect = [
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.SEVEN, Suit.SPADES),
        Card(Rank.NINE, Suit.CLUBS),
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.SEVEN, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.SIX, Suit.DIAMONDS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.SIX, Suit.HEARTS),
        Card(Rank.TEN, Suit.CLUBS),
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.TEN, Suit.HEARTS),
    ]
    return mock


@pytest.fixture
def seven_of_hearts():
    return game.Card(Rank.SEVEN, Suit.HEARTS)


@pytest.fixture
def six_of_spades():
    return game.Card(Rank.SIX, Suit.SPADES)


@pytest.fixture
def ace_of_spades():
    return game.Card(Rank.ACE, Suit.SPADES)


@pytest.fixture
def six_of_clubs():
    return game.Card(Rank.SIX, Suit.CLUBS)


@pytest.fixture
def nine_of_clubs():
    return game.Card(Rank.NINE, Suit.CLUBS)


@pytest.fixture
def king_of_clubs():
    return game.Card(Rank.KING, Suit.CLUBS)


@pytest.fixture
def hand_after_playing():
    return {
        game.Card(Rank.EIGHT, Suit.HEARTS),
        game.Card(Rank.NINE, Suit.HEARTS),
        game.Card(Rank.SEVEN, Suit.CLUBS),
        game.Card(Rank.EIGHT, Suit.CLUBS),
        game.Card(Rank.NINE, Suit.CLUBS),
        game.Card(Rank.TEN, Suit.DIAMONDS),
        game.Card(Rank.JACK, Suit.DIAMONDS),
        game.Card(Rank.QUEEN, Suit.DIAMONDS),
    }


@pytest.fixture
def sorted_cards():
    return [
        game.Card(Rank.NINE, Suit.CLUBS),
        game.Card(Rank.EIGHT, Suit.CLUBS),
        game.Card(Rank.SEVEN, Suit.CLUBS),
        game.Card(Rank.NINE, Suit.HEARTS),
        game.Card(Rank.EIGHT, Suit.HEARTS),
        game.Card(Rank.QUEEN, Suit.DIAMONDS),
        game.Card(Rank.JACK, Suit.DIAMONDS),
        game.Card(Rank.TEN, Suit.DIAMONDS),
    ]


@pytest.fixture
def hand_without_bid(hand_after_playing, seven_of_hearts):
    return hand_after_playing | {seven_of_hearts}


@pytest.fixture
def initial_hand(bid, hand_without_bid):
    return bid | hand_without_bid


@pytest.fixture
def player_before_bidding(initial_hand):
    return game.Player(initial_hand)


@pytest.fixture
def player_after_bidding(player_before_bidding, bid):
    player_before_bidding.make_bid(bid)
    return player_before_bidding


@pytest.fixture
def player_with_one_card(seven_of_hearts):
    return game.Player({seven_of_hearts})


@pytest.fixture
def game_state_first_player_made_bid(game_state_after_bidding):
    game_state_after_bidding.PLAYERS[0].tricks_won = 3
    game_state_after_bidding.PLAYERS[1].tricks_won = 1
    game_state_after_bidding.PLAYERS[2].tricks_won = 5
    for player in game_state_after_bidding.PLAYERS.values():
        player.hand = set()
    return game_state_after_bidding


@pytest.fixture
def game_state_two_players_made_bid(game_state_after_bidding, different_three_bids):
    game_state_after_bidding.PLAYERS[0].tricks_won = 4
    game_state_after_bidding.PLAYERS[1].tricks_won = 4
    game_state_after_bidding.PLAYERS[2].tricks_won = 1
    game_state_after_bidding.stage = game.GameStage.DONE
    for player_num, player in game_state_after_bidding.PLAYERS.items():
        player.hand = set()
        player.bid = different_three_bids[player_num]
    return game_state_after_bidding


@pytest.fixture
def game_state_after_dealing(three_hands_of_nine):
    new_state = game.GameState(random_seed=ARBITRARY_SEED)
    new_state.stage = game.GameStage.PLAYING
    for i in range(len(new_state.PLAYERS)):
        new_state.PLAYERS[i].hand = three_hands_of_nine[i]
    new_state.TRUMP_SUIT = Suit.CLUBS

    return new_state


@pytest.fixture
def game_state_after_dealing_spades_trump(game_state_after_dealing):
    game_state_after_dealing.TRUMP_SUIT = Suit.SPADES
    return game_state_after_dealing


def test_game_state(game_state_after_dealing_spades_trump):
    assert game_state_after_dealing_spades_trump.next_to_play == 0
    assert game_state_after_dealing_spades_trump.current_trick["lead_player"] == 0


@pytest.fixture
def game_state_after_bidding(game_state_after_dealing, three_bids_of_three):
    for i in range(len(game_state_after_dealing.PLAYERS)):
        game_state_after_dealing.PLAYERS[i].bid = three_bids_of_three[i]
    return game_state_after_dealing


@pytest.fixture
def six_of_hearts():
    return game.Card(Rank.SIX, Suit.HEARTS)


@pytest.fixture
def ten_of_hearts():
    return game.Card(Rank.TEN, Suit.HEARTS)


@pytest.fixture
def trick_of_two_cards(seven_of_hearts, six_of_spades) -> game.Trick:
    return {
        "cards": {0: seven_of_hearts, 1: six_of_spades},
        "lead_player": 0,
        "winner": None,
    }


@pytest.fixture
def trick_of_six_club_and_nine_club(six_of_clubs, nine_of_clubs) -> game.Trick:
    return {
        "cards": {0: six_of_clubs, 1: nine_of_clubs},
        "lead_player": 0,
        "winner": None,
    }


@pytest.fixture
def trick_of_six_nine_and_king_of_clubs(
    six_of_clubs, nine_of_clubs, king_of_clubs
) -> game.Trick:
    return {
        "cards": {0: six_of_clubs, 1: nine_of_clubs, 2: king_of_clubs},
        "lead_player": 0,
        "winner": None,
    }


@pytest.fixture
def trick_of_three_cards(seven_of_hearts, six_of_spades, six_of_hearts) -> game.Trick:
    return {
        "cards": {0: seven_of_hearts, 1: six_of_spades, 2: six_of_hearts},
        "lead_player": 0,
        "winner": None,
    }


@pytest.fixture
def game_state_with_one_trick(game_state_after_dealing, trick_of_three_cards):
    game_state_after_dealing.current_trick = trick_of_three_cards
    game_state_after_dealing.stage = game.GameStage.PLAYING
    return game_state_after_dealing


@pytest.fixture
def game_state_with_two_card_trick(game_state_after_dealing, trick_of_two_cards):
    game_state_after_dealing.current_trick = trick_of_two_cards
    game_state_after_dealing.next_to_play = 2
    game_state_after_dealing.stage = game.GameStage.PLAYING
    return game_state_after_dealing


@pytest.fixture
def game_state_with_six_club_and_nine_club(
    game_state_after_dealing, trick_of_six_club_and_nine_club
):
    game_state_after_dealing.current_trick = trick_of_six_club_and_nine_club
    return game_state_after_dealing


@pytest.fixture
def game_state_with_six_nine_and_king_of_clubs(
    game_state_after_dealing, trick_of_six_nine_and_king_of_clubs
):
    game_state_after_dealing.current_trick = trick_of_six_nine_and_king_of_clubs
    return game_state_after_dealing


@pytest.fixture
def game_state_after_one_card(game_state_after_dealing, ace_of_spades):
    state = game_state_after_dealing.copy_state()
    state.current_trick["cards"][state.next_to_play] = ace_of_spades
    state.PLAYERS[state.next_to_play].hand.remove(ace_of_spades)
    state.next_to_play = 1
    return state


@pytest.fixture
def three_hands_of_nine(ace_of_spades, six_of_hearts, ten_of_hearts):
    hand0 = {
        game.Card(Rank.JACK, Suit.SPADES),
        ace_of_spades,
        game.Card(Rank.QUEEN, Suit.SPADES),
        game.Card(Rank.SIX, Suit.SPADES),
        game.Card(Rank.ACE, Suit.DIAMONDS),
        game.Card(Rank.EIGHT, Suit.DIAMONDS),
        game.Card(Rank.QUEEN, Suit.HEARTS),
        game.Card(Rank.ACE, Suit.CLUBS),
        game.Card(Rank.SIX, Suit.CLUBS),
    }
    hand1 = {
        game.Card(Rank.KING, Suit.DIAMONDS),
        game.Card(Rank.KING, Suit.SPADES),
        game.Card(Rank.KING, Suit.HEARTS),
        game.Card(Rank.ACE, Suit.HEARTS),
        game.Card(Rank.SEVEN, Suit.HEARTS),
        game.Card(Rank.JACK, Suit.HEARTS),
        game.Card(Rank.TEN, Suit.CLUBS),
        game.Card(Rank.SEVEN, Suit.CLUBS),
        game.Card(Rank.NINE, Suit.CLUBS),
    }
    hand2 = {
        game.Card(Rank.JACK, Suit.DIAMONDS),
        game.Card(Rank.SIX, Suit.DIAMONDS),
        game.Card(Rank.SEVEN, Suit.SPADES),
        six_of_hearts,
        ten_of_hearts,
        game.Card(Rank.EIGHT, Suit.CLUBS),
        game.Card(Rank.QUEEN, Suit.CLUBS),
        game.Card(Rank.KING, Suit.CLUBS),
        game.Card(Rank.JACK, Suit.CLUBS),
    }
    return hand0, hand1, hand2


@pytest.fixture
def sorted_first_hand(three_hands_of_nine):
    return game_display.get_sorted_cards(three_hands_of_nine[0])


@pytest.fixture
def three_bids_of_three():
    bid1 = {
        game.Card(Rank.TEN, Suit.SPADES),
        game.Card(Rank.NINE, Suit.SPADES),
        game.Card(Rank.EIGHT, Suit.SPADES),
    }
    bid2 = {
        game.Card(Rank.NINE, Suit.DIAMONDS),
        game.Card(Rank.QUEEN, Suit.DIAMONDS),
        game.Card(Rank.NINE, Suit.HEARTS),
    }
    bid3 = {
        game.Card(Rank.SEVEN, Suit.DIAMONDS),
        game.Card(Rank.TEN, Suit.DIAMONDS),
        game.Card(Rank.EIGHT, Suit.HEARTS),
    }
    return bid1, bid2, bid3


@pytest.fixture
def different_three_bids():
    bid1 = {
        game.Card(Rank.ACE, Suit.CLUBS),
        game.Card(Rank.KING, Suit.HEARTS),
        game.Card(Rank.QUEEN, Suit.DIAMONDS),
    }
    bid2 = {
        game.Card(Rank.JACK, Suit.HEARTS),
        game.Card(Rank.TEN, Suit.HEARTS),
        game.Card(Rank.NINE, Suit.DIAMONDS),
    }
    bid3 = {
        game.Card(Rank.EIGHT, Suit.DIAMONDS),
        game.Card(Rank.SEVEN, Suit.SPADES),
        game.Card(Rank.SIX, Suit.DIAMONDS),
    }
    return bid1, bid2, bid3


@pytest.fixture
def ten_of_hearts_string():
    return "TH"
