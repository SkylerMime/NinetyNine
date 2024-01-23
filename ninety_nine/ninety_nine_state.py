import dataclasses
import random
from ninety_nine.constants import Rank, Suit, GameStage
from typing import Dict
from dataclasses import dataclass

type Scores = dict[int, int]


@dataclass
class Card:
    rank: Rank
    suit: Suit

    def __lt__(self, other):
        if self.suit == other.suit:
            return self.rank < other.rank
        else:
            return self.suit < other.suit

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False

    def __hash__(self):
        return hash((self.rank, self.suit))


@dataclass
class Trick:
    cards: dict
    lead_player: int
    winner: int | None


class Player:
    def __init__(self, hand_cards: set | None = None):
        if hand_cards is None:
            hand_cards = set()
        self.hand = hand_cards
        self.bid = set()
        self.tricks_won = 0
        self.state = GameStage.BIDDING

    def make_bid(self, bid_cards: set):
        self.hand = self.hand - bid_cards
        self.bid = bid_cards
        self.state = GameStage.PLAYING

    def play_card(self, card_to_play: Card):
        try:
            self.hand.remove(card_to_play)
            if len(self.hand) < 1:
                self.state = GameStage.DONE
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
    def __init__(self, random_seed=None, start_new_game=True):
        self.TRUMP_SUIT = None
        self.current_lead: int = 0
        self.current_trick: Trick = Trick({}, 0, None)
        self.PLAYERS: Dict[int, Player] = {}
        self.trick_history = []
        self.next_to_play: int = 0
        self.stage = GameStage.BIDDING
        if start_new_game:
            self.start_new_game(random_seed)

    def start_new_game(self, random_seed=None):
        random.seed(random_seed)
        # Create a list with all the cards
        all_cards = list(get_all_cards())
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
        new_state = GameState(start_new_game=False)
        new_state.TRUMP_SUIT = self.TRUMP_SUIT
        new_state.current_lead = self.current_lead
        new_state.current_trick = dataclasses.replace(self.current_trick)
        new_state.current_trick.cards = self.current_trick.cards.copy()
        new_state.PLAYERS = {
            player_num: player.copy() for player_num, player in self.PLAYERS.items()
        }
        new_state.trick_history = self.trick_history.copy()
        new_state.next_to_play = self.next_to_play
        new_state.stage = self.stage
        return new_state

    def get_current_trick_winner(self):
        return get_trick_winner(self.current_trick, self.TRUMP_SUIT)

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


def get_all_cards(suits: set = Suit, ranks: set = Rank):
    return {Card(rank, suit) for rank in ranks for suit in suits}


def is_full(trick: Trick):
    for playerNum in (0, 1, 2):
        if playerNum not in trick.cards.keys():
            return False
    else:
        return True


def get_legal_card_plays(game_state: GameState, player_num: int | None):
    if player_num not in game_state.PLAYERS.keys():
        raise KeyError(f"player is {player_num}, but it must be 0, 1, or 2")
    if game_state.next_to_play != player_num:
        raise KeyError("it is not this player's turn")

    current_player: Player = game_state.PLAYERS[player_num]

    if game_state.current_lead == player_num:
        return current_player.hand

    led_card: Card = game_state.current_trick.cards[game_state.current_lead]
    led_suit = led_card.suit

    # we must follow suit if possible
    cards_in_led_suit = {card for card in current_player.hand if card.suit == led_suit}

    if len(cards_in_led_suit) > 0:
        return cards_in_led_suit

    # otherwise we may play any card
    else:
        return current_player.hand


def get_trick_winner(trick: Trick, trump_suit: Suit):
    lead_player_num = trick.lead_player
    trick_cards = trick.cards
    highest_card_player = lead_player_num
    highest_lead_rank = trick_cards[highest_card_player].rank
    highest_trump_rank: Rank = Rank.SIX
    lead_card: Card = trick_cards[lead_player_num]
    lead_trumped = False
    # Was the card trumped?
    # If so, highest trump wins
    # If not, highest lead suit wins
    for player, card in trick_cards.items():
        if card.suit == trump_suit and card.rank >= highest_trump_rank:
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


def make_card_play(game_state: GameState, player: int, card: Card):
    if is_full(game_state.current_trick):
        raise ValueError("this trick is full")
    if player not in game_state.PLAYERS.keys():
        raise KeyError(f"player is {player}, but it must be 0, 1, or 2")
    if game_state.next_to_play != player:
        raise KeyError("it is not this player's turn")

    next_state = game_state.copy_state()

    current_player: Player = next_state.PLAYERS[player]
    current_player.play_card(card)
    next_state.current_trick.cards[player] = card

    if is_full(next_state.current_trick):
        next_state.next_to_play = None
    else:
        next_state.next_to_play = (game_state.next_to_play + 1) % len(
            game_state.PLAYERS
        )

    return next_state


def finish_trick(game_state: GameState):
    next_state = game_state.copy_state()
    if not is_full(next_state.current_trick):
        raise KeyError("Some players still need to play")

    trick_winner = next_state.get_current_trick_winner()
    next_state.current_trick.winner = trick_winner
    next_state.trick_history.append(next_state.current_trick)
    next_state.PLAYERS[trick_winner].tricks_won += 1

    next_state.current_trick = Trick(cards={}, lead_player=None, winner=None)

    if game_is_over(next_state):
        next_state.current_lead = None
        next_state.next_to_play = None
    else:
        next_state.current_lead = trick_winner
        next_state.next_to_play = trick_winner

    next_state.current_trick.lead_player = next_state.current_lead

    return next_state


def bid_value(bid: set | list):
    contracted_tricks = 0
    for card in bid:
        contracted_tricks += card.suit.value
    return contracted_tricks


def game_is_over(game_state: GameState):
    if len(game_state.current_trick.cards) > 0:
        return False
    for player in game_state.PLAYERS.values():
        if len(player.hand) > 0:
            return False
    return True


def get_scores(final_state: GameState) -> Scores:
    if not game_is_over(final_state):
        raise KeyError("all cards should be played")
    if len(final_state.current_trick.cards) > 0:
        raise KeyError("current trick should be finalized")

    players_making_bid = [
        player
        for player in final_state.PLAYERS.values()
        if player.tricks_won == bid_value(player.bid)
    ]

    bid_bonus = 0
    if len(players_making_bid) == 1:
        bid_bonus = 30
    elif len(players_making_bid) == 2:
        bid_bonus = 20
    elif len(players_making_bid) == 3:
        bid_bonus = 10

    scores: Scores = {
        player_num: player.tricks_won + bid_bonus * (player in players_making_bid)
        for player_num, player in final_state.PLAYERS.items()
    }

    return scores
