import pytest
from ninety_nine import ninety_nine_state as game
from ninety_nine.constants import Rank, Suit, PlayerState

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


class TestPLayer:
    def test_player_bid_removes_cards(self, player_after_bidding, hand_without_bid):
        assert player_after_bidding.hand == hand_without_bid

    def test_player_bid_leaves_nine(self, player_after_bidding):
        assert len(player_after_bidding.hand) == 9

    def test_player_bid_changes_state(self, player_after_bidding):
        assert player_after_bidding.state == PlayerState.PLAYING

    def test_player_card_play(
        self, player_after_bidding, seven_of_hearts, hand_after_playing
    ):
        player_after_bidding.play_card(seven_of_hearts)
        assert player_after_bidding.hand == hand_after_playing

    def test_player_last_card_changes_state(
        self, seven_of_hearts, player_with_one_card
    ):
        player_with_one_card.play_card(seven_of_hearts)
        assert player_with_one_card.state == PlayerState.DONE

    def test_player_wrong_card_throws_error(self, player_after_bidding, six_of_spades):
        with pytest.raises(KeyError):
            player_after_bidding.play_card(six_of_spades)


@pytest.fixture
def game_state_after_dealing(three_hands_of_nine):
    new_state = game.GameState()
    new_state.start_new_game(ARBITRARY_SEED)
    for i in range(len(new_state.PLAYERS)):
        new_state.PLAYERS[i].hand = three_hands_of_nine[i]
    new_state.TRUMP_SUIT = Suit.CLUBS

    return new_state


@pytest.fixture
def six_of_hearts():
    return game.Card(Rank.SIX, Suit.HEARTS)


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
def three_hands_of_nine(ace_of_spades):
    hand1 = {
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
    hand2 = {
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
    hand3 = {
        game.Card(Rank.JACK, Suit.DIAMONDS),
        game.Card(Rank.SIX, Suit.DIAMONDS),
        game.Card(Rank.SEVEN, Suit.SPADES),
        game.Card(Rank.SIX, Suit.HEARTS),
        game.Card(Rank.TEN, Suit.HEARTS),
        game.Card(Rank.EIGHT, Suit.CLUBS),
        game.Card(Rank.ACE, Suit.CLUBS),
        game.Card(Rank.KING, Suit.CLUBS),
        game.Card(Rank.JACK, Suit.CLUBS),
    }
    return hand1, hand2, hand3


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


class TestGameState:
    def test_highest_heart_wins_heart_trick(self, game_state_with_one_trick):
        game_state_with_one_trick.TRUMP_SUIT = Suit.CLUBS
        game_state_with_one_trick.current_lead = 2
        assert game_state_with_one_trick.get_current_trick_winner() == 0

    def test_spades_trump_beats_high_cards(self, game_state_with_one_trick):
        game_state_with_one_trick.TRUMP_SUIT = Suit.SPADES
        game_state_with_one_trick.current_lead = 2
        assert game_state_with_one_trick.get_current_trick_winner() == 1

    def test_copy_state_leaves_original_trick_unchanged(self, game_state_after_dealing, ace_of_spades):
        original_state = game_state_after_dealing
        new_state = game_state_after_dealing.copy_state()
        new_state.current_trick[0] = ace_of_spades
        assert len(original_state.current_trick) == 0

    def test_copy_state_leaves_original_lead_unchanged(self, game_state_after_dealing):
        original_state = game_state_after_dealing
        new_state = game_state_after_dealing.copy_state()
        new_state.current_lead = 3
        assert original_state.current_lead == 0


class TestFunctions:
    def test_full_trick_is_full_returns_true(self, trick_of_three_cards):
        assert game.is_full(trick_of_three_cards) is True

    def test_partial_trick_is_full_returns_false(self, trick_of_two_cards):
        assert game.is_full(trick_of_two_cards) is False

    def test_play_card_leaves_original_state_unchanged(
        self, game_state_after_dealing, ace_of_spades, three_hands_of_nine
    ):
        original_state = game_state_after_dealing
        player_num = 0
        player_card = ace_of_spades
        new_state = game.make_card_play(original_state, player_num, player_card)
        assert new_state != game_state_after_dealing
        assert original_state == game_state_after_dealing

    def test_play_card_to_incomplete_trick_returns_new_state(
        self, game_state_after_dealing, game_state_after_one_card, ace_of_spades
    ):
        player_num = 0
        new_state = game.make_card_play(
            game_state_after_dealing, player_num, ace_of_spades
        )
        assert new_state == game_state_after_one_card

    def test_play_card_to_finish_trick_sets_new_lead(self, game_state_with_two_card_trick, six_of_hearts):
        player_to_move = 2
        game_state_with_two_card_trick.current_lead = 2
        game_state_with_two_card_trick.PLAYERS[player_to_move].hand.add(six_of_hearts)
        game_state_with_two_card_trick.next_to_play = player_to_move
        finish_trick_state = game.make_card_play(game_state_with_two_card_trick, player_to_move, six_of_hearts)
        assert finish_trick_state.current_lead == 0

    def test_play_card_to_finish_trick_increments_wins(self, game_state_with_two_card_trick, six_of_hearts):
        player_to_move = 2
        player_to_win = 0
        game_state_with_two_card_trick.current_lead = 2
        game_state_with_two_card_trick.PLAYERS[player_to_move].hand.add(six_of_hearts)
        game_state_with_two_card_trick.PLAYERS[player_to_win].tricks_won = 4
        game_state_with_two_card_trick.next_to_play = player_to_move
        finish_trick_state = game.make_card_play(game_state_with_two_card_trick, player_to_move, six_of_hearts)
        assert finish_trick_state.PLAYERS[player_to_win].tricks_won == 5
        assert game_state_with_two_card_trick.PLAYERS[player_to_win].tricks_won == 4
