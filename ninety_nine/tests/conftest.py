import pytest
from ninety_nine import ninety_nine_state as game
from ninety_nine.constants import Rank, Suit

ARBITRARY_SEED = 5


@pytest.fixture
def bid():
    return {
        game.Card(Rank.ACE, Suit.SPADES),
        game.Card(Rank.KING, Suit.SPADES),
        game.Card(Rank.QUEEN, Suit.SPADES),
    }


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
def hand_without_bid(hand_after_playing, seven_of_hearts):
    return hand_after_playing | {seven_of_hearts}


@pytest.fixture
def initial_hand(bid, hand_without_bid):
    return bid | hand_without_bid


@pytest.fixture
def player_after_bidding(initial_hand, bid):
    player = game.Player(initial_hand)
    player.make_bid(bid)
    return player


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
    for player_num, player in game_state_after_bidding.PLAYERS.items():
        player.hand = set()
        player.bid = different_three_bids[player_num]
    return game_state_after_bidding


@pytest.fixture
def game_state_after_dealing(three_hands_of_nine):
    new_state = game.GameState()
    new_state.start_new_game(ARBITRARY_SEED)
    for i in range(len(new_state.PLAYERS)):
        new_state.PLAYERS[i].hand = three_hands_of_nine[i]
    new_state.TRUMP_SUIT = Suit.CLUBS

    return new_state


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
def trick_of_two_cards(seven_of_hearts, six_of_spades):
    return {0: seven_of_hearts, 1: six_of_spades}


@pytest.fixture
def trick_of_three_cards(seven_of_hearts, six_of_spades, six_of_hearts):
    return {0: seven_of_hearts, 1: six_of_spades, 2: six_of_hearts}


@pytest.fixture
def game_state_with_one_trick(game_state_after_dealing, trick_of_three_cards):
    game_state_after_dealing.current_trick = trick_of_three_cards
    return game_state_after_dealing


@pytest.fixture
def game_state_with_two_card_trick(game_state_after_dealing, trick_of_two_cards):
    game_state_after_dealing.current_trick = trick_of_two_cards
    return game_state_after_dealing


@pytest.fixture
def game_state_after_one_card(game_state_after_dealing, ace_of_spades):
    state = game_state_after_dealing.copy_state()
    state.current_trick[state.next_to_play] = ace_of_spades
    state.PLAYERS[state.next_to_play].hand.remove(ace_of_spades)
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
        game.Card(Rank.ACE, Suit.CLUBS),
        game.Card(Rank.KING, Suit.CLUBS),
        game.Card(Rank.JACK, Suit.CLUBS),
    }
    return hand0, hand1, hand2


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
