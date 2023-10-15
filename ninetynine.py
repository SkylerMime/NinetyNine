from enum import Enum
import random

class PlayerState(Enum):
    WAITING = 0
    PLAYING = 1
    DONE = 2

class Suit(Enum):
    DIAMONDS = 0
    SPADES = 1
    HEARTS = 2
    CLUBS = 3

class Rank(int, Enum):
    SIX = 0
    SEVEN = 1
    EIGHT = 2
    NINE = 3
    TEN = 4
    JACK = 5
    QUEEN = 6
    KING = 7
    ACE = 8

class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

class Player:
    def makeBid(self, bidCards: set):
        self.hand = self.hand - bidCards
        self.bid = bidCards
        self.state = PlayerState.PLAYING

    def playCard(self, cardToPlay: Card):
        try:
            self.hand.remove(cardToPlay)
            if len(self.hand) < 1:
                self.state = PlayerState.DONE
        except KeyError:
            raise KeyError(
                "card must be an element of the player's hand"
            )

    def __init__(self, handCards: set = set()):
        self.hand = handCards
        self.bid = set()
        self.state = PlayerState.WAITING

class GameState:
    def startNewGame(self):
        # Create a list with all the cards
        allCards = []
        for suit in Suit:
            for rank in Rank:
                card = Card(rank, suit)
                allCards.append(card)
        # Shuffle the cards
        random.shuffle(allCards)
        # Deal the cards
        eldestHand = set()
        middleHand = set()
        youngestHand = set()
        while len(allCards) > 0:
            eldestHand.add(allCards.pop)
            middleHand.add(allCards.pop)
            youngestHand.add(allCards.pop)
        eldest = Player(eldestHand)
        middle = Player(middleHand)
        youngest = Player(youngestHand)
        self.players = {0: eldest, 1: middle, 2: youngest}
        # Set the state
        self.currentTrick = 0
        self.currentLead = 0

    # def playCard(self, player: Player, card: Card):
    #     try:
    #         player.playCard(card)

    #     except KeyError:
    #         raise

    def __init__(self):
        startNewGame()