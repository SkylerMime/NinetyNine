import pytest
from ninety_nine import ninety_nine_state as game
from ninety_nine.constants import Suit, GameStage
from ninety_nine.ninety_nine_state import Trick


class TestPLayer:
    def test_player_bid_removes_cards(self, player_after_bidding, hand_without_bid):
        assert player_after_bidding.hand == hand_without_bid

    def test_player_bid_leaves_nine(self, player_after_bidding):
        assert len(player_after_bidding.hand) == 9

    def test_player_bid_changes_state(self, player_after_bidding):
        assert player_after_bidding.state == GameStage.PLAYING

    def test_player_card_play(
        self, player_after_bidding, seven_of_hearts, hand_after_playing
    ):
        player_after_bidding.play_card(seven_of_hearts)
        assert player_after_bidding.hand == hand_after_playing

    def test_player_last_card_changes_state(
        self, seven_of_hearts, player_with_one_card
    ):
        player_with_one_card.play_card(seven_of_hearts)
        assert player_with_one_card.state == GameStage.DONE

    def test_player_wrong_card_throws_error(self, player_after_bidding, six_of_spades):
        with pytest.raises(KeyError):
            player_after_bidding.play_card(six_of_spades)


class TestGameState:
    def test_highest_heart_wins_heart_trick(self, game_state_with_one_trick):
        game_state_with_one_trick.TRUMP_SUIT = Suit.CLUBS
        game_state_with_one_trick.current_lead = 2
        assert game_state_with_one_trick.get_current_trick_winner() == 0

    def test_spades_trump_beats_high_cards(self, game_state_with_one_trick):
        game_state_with_one_trick.TRUMP_SUIT = Suit.SPADES
        game_state_with_one_trick.current_lead = 2
        assert game_state_with_one_trick.get_current_trick_winner() == 1

    def test_king_beats_six_and_nine(self, game_state_with_six_nine_and_king_of_clubs):
        game_state_with_six_nine_and_king_of_clubs.current_lead = 0
        assert (
            game_state_with_six_nine_and_king_of_clubs.get_current_trick_winner() == 2
        )

    def test_copy_state_leaves_original_trick_unchanged(
        self, game_state_after_dealing, ace_of_spades
    ):
        original_state = game_state_after_dealing
        new_state = game_state_after_dealing.copy_state()
        new_state.current_trick.cards[0] = ace_of_spades
        assert len(original_state.current_trick.cards) == 0

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

    @pytest.mark.parametrize(
        "game_state,new_card,expected_lead",
        [
            ("game_state_with_two_card_trick", "six_of_hearts", 0),
            ("game_state_with_six_club_and_nine_club", "king_of_clubs", 2),
        ],
    )
    def test_play_card_to_finish_trick_sets_new_lead(
        self, game_state, new_card, expected_lead, request
    ):
        game_state = request.getfixturevalue(game_state)
        new_card = request.getfixturevalue(new_card)
        player_to_move = 2
        game_state.current_lead = 0
        game_state.PLAYERS[player_to_move].hand.add(new_card)
        game_state.next_to_play = player_to_move
        finish_trick_state = game.make_card_play(game_state, player_to_move, new_card)
        finish_trick_state = game.finish_trick(finish_trick_state)
        assert finish_trick_state.current_lead == expected_lead
        assert finish_trick_state.next_to_play == expected_lead

    def test_play_card_to_finish_trick_increments_wins(
        self, game_state_with_two_card_trick, six_of_hearts
    ):
        player_to_move = 2
        player_to_win = 0
        game_state_with_two_card_trick.current_lead = 0
        game_state_with_two_card_trick.PLAYERS[player_to_move].hand.add(six_of_hearts)
        game_state_with_two_card_trick.PLAYERS[player_to_win].tricks_won = 4
        game_state_with_two_card_trick.next_to_play = player_to_move
        finish_trick_state = game.make_card_play(
            game_state_with_two_card_trick, player_to_move, six_of_hearts
        )
        finish_trick_state = game.finish_trick(finish_trick_state)
        assert finish_trick_state.PLAYERS[player_to_win].tricks_won == 5
        assert game_state_with_two_card_trick.PLAYERS[player_to_win].tricks_won == 4

    def test_get_legal_moves_for_heart_trick(
        self, game_state_with_two_card_trick, six_of_hearts, ten_of_hearts
    ):
        player_to_move = 2
        game_state_with_two_card_trick.current_lead = 0
        game_state_with_two_card_trick.next_to_play = 2
        legal_cards_to_play = {six_of_hearts, ten_of_hearts}
        assert (
            game.get_legal_card_plays(game_state_with_two_card_trick, player_to_move)
            == legal_cards_to_play
        )

    def test_get_legal_moves_for_void_suit(
        self, game_state_with_two_card_trick, six_of_hearts, ten_of_hearts
    ):
        player_to_move_num = 2
        game_state_with_two_card_trick.current_lead = 0
        game_state_with_two_card_trick.next_to_play = 2
        player_to_move = game_state_with_two_card_trick.PLAYERS[player_to_move_num]
        player_to_move.hand.remove(six_of_hearts)
        player_to_move.hand.remove(ten_of_hearts)
        legal_cards_to_play = player_to_move.hand.copy()
        assert (
            game.get_legal_card_plays(
                game_state_with_two_card_trick, player_to_move_num
            )
            == legal_cards_to_play
        )

    def test_get_legal_moves_for_empty_trick(self, game_state_after_bidding):
        player_to_move_num = 0
        game_state_after_bidding.current_lead = 0
        game_state_after_bidding.next_to_play = 0
        player_to_move: game.Player = game_state_after_bidding.PLAYERS[
            player_to_move_num
        ]
        legal_cards_to_play = player_to_move.hand.copy()
        assert (
            game.get_legal_card_plays(game_state_after_bidding, player_to_move_num)
            == legal_cards_to_play
        )

    def test_bid_value_of_three(self, bid):
        assert game.bid_value(bid) == 3

    def test_outcome_incomplete_game(self, game_state_with_two_card_trick):
        with pytest.raises(KeyError):
            game.get_scores(game_state_with_two_card_trick)

    def test_outcome_one_winner(self, game_state_first_player_made_bid):
        assert game.get_scores(game_state_first_player_made_bid) == {0: 33, 1: 1, 2: 5}

    def test_outcome_two_winners(self, game_state_two_players_made_bid):
        assert game.get_scores(game_state_two_players_made_bid) == {0: 4, 1: 24, 2: 21}

    def test_get_trick_winner_needs_only_the_trick(
        self, ace_of_spades, ten_of_hearts, seven_of_hearts
    ):
        trick = Trick(
            {
                0: ace_of_spades,
                1: ten_of_hearts,
                2: seven_of_hearts,
            },
            0,
            None,
        )
        assert game.get_trick_winner(trick, Suit.CLUBS) == 0

    def test_get_some_cards(self, ranks_subset, suits_subset, cards_subset):
        assert game.get_all_cards(suits_subset, ranks_subset) == cards_subset
