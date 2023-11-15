import random
from copy import copy
from ninety_nine.constants import Rank, Suit, PlayerState
import typing


class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit


class Player:
    def __init__(self, hand_cards: set | None = None):
        if hand_cards is None:
            hand_cards = set()
        self.hand = hand_cards
        self.bid = set()
        self.tricks_won = 0
        self.state = PlayerState.WAITING

    def make_bid(self, bid_cards: set):
        self.hand = self.hand - bid_cards
        self.bid = bid_cards
        self.state = PlayerState.PLAYING

    def play_card(self, card_to_play: Card):
        try:
            self.hand.remove(card_to_play)
            if len(self.hand) < 1:
                self.state = PlayerState.DONE
        except KeyError:
            raise KeyError("card must be an element of the player's hand")

    def copy(self):
        new_player = Player()
        new_player.hand = self.hand.copy()
        new_player.bid = self.bid.copy()
        new_player.tricks_won = self.tricks_won
        new_player.state = self.state
        return new_player

    def __eq__(self, other):
        if isinstance(other, Player):
            return (
                self.hand == other.hand
                and self.bid == other.bid
                and self.tricks_won == other.tricks_won
                and self.state == other.state
            )
        return False


class GameState:
    def __init__(self):
        self.TRUMP_SUIT = None
        self.current_lead = None
        self.current_trick: dict = {}
        self.PLAYERS = {}
        self.trick_history = []
        self.next_to_play = None

    def start_new_game(self, random_seed=None):
        random.seed(random_seed)
        # Create a list with all the cards
        all_cards = []
        for suit in Suit:
            for rank in Rank:
                card = Card(rank, suit)
                all_cards.append(card)
        eldest_hand, middle_hand, youngest_hand = get_three_shuffled_hands(
            all_cards, random_seed
        )
        eldest = Player(eldest_hand)
        middle = Player(middle_hand)
        youngest = Player(youngest_hand)
        self.PLAYERS = {0: eldest, 1: middle, 2: youngest}
        self.current_lead = 0
        self.next_to_play = 0
        self.TRUMP_SUIT = random.choice(list(Suit))

    def copy_state(self):
        new_state = GameState()
        new_state.TRUMP_SUIT = self.TRUMP_SUIT
        new_state.current_lead = self.current_lead
        new_state.current_trick = self.current_trick.copy()
        for player_num in range(len(self.PLAYERS)):
            new_state.PLAYERS[player_num] = self.PLAYERS[player_num].copy()
        new_state.trick_history = self.trick_history.copy()
        new_state.next_to_play = self.next_to_play
        return new_state

    def get_current_trick_winner(self):
        highest_card_player = self.current_lead
        highest_lead_rank = self.current_trick[highest_card_player].rank
        highest_trump_rank: Rank = Rank.SIX
        lead_card: Card = self.current_trick[self.current_lead]
        lead_trumped = False
        # Was the card trumped?
        # If so, highest trump wins
        # If not, highest lead suit wins
        for player, card in self.current_trick.items():
            if card.suit == self.TRUMP_SUIT and card.rank >= highest_trump_rank:
                lead_trumped = True
                highest_card_player = player
                highest_trump_rank = card.rank
            if (
                not lead_trumped
                and card.suit == lead_card.suit
                and card.rank > highest_lead_rank
            ):
                highest_card_player = player
                highest_lead_rank = card.rank
        return highest_card_player

    def __eq__(self, other):
        if isinstance(other, GameState):
            return (
                self.TRUMP_SUIT == other.TRUMP_SUIT
                and self.current_lead == other.current_lead
                and self.current_trick == other.current_trick
                and self.PLAYERS[0] == other.PLAYERS[0]
                and self.PLAYERS[1] == other.PLAYERS[1]
                and self.PLAYERS[2] == other.PLAYERS[2]
                and self.trick_history == other.trick_history
                and self.next_to_play == other.next_to_play
            )
        return False


def get_three_shuffled_hands(cards_to_deal: list[Card], random_seed=None):
    random.seed(random_seed)
    # Shuffle the cards
    random.shuffle(cards_to_deal)
    # Deal the cards
    first_hand = set()
    second_hand = set()
    third_hand = set()
    while len(cards_to_deal) > 0:
        first_hand.add(cards_to_deal.pop())
        second_hand.add(cards_to_deal.pop())
        third_hand.add(cards_to_deal.pop())
    return first_hand, second_hand, third_hand


def is_full(trick: dict):
    for playerNum in (0, 1, 2):
        if playerNum not in trick.keys():
            return False
    else:
        return True


def make_card_play(game_state: GameState, player: int, card: Card):
    if player not in game_state.PLAYERS.keys():
        raise KeyError("player must be 0, 1, or 2")
    if game_state.next_to_play != player:
        raise KeyError("it is not this player's turn")

    next_state = game_state.copy_state()

    current_player: Player = game_state.PLAYERS[player]
    current_player.play_card(card)
    current_trick = game_state.current_trick
    next_state.current_trick[player] = card

    if is_full(next_state.current_trick):
        next_state.trick_history.append(next_state.current_trick)
        trick_winner = next_state.get_current_trick_winner()
        next_state.current_lead = trick_winner
        next_state.PLAYERS[trick_winner].tricks_won += 1

        next_state.current_trick = {}

    return next_state
