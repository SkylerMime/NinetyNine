from enum import Enum


NUM_CARDS_IN_BID = 3
NUM_TRICKS = 9
NUM_PLAYERS = 3


class PlayerTypes(Enum):
    HUMAN = 0
    RANDOM = 1
    MONTE_CARLO_AI = 2
    TRICK_COMPLETE = 3
    WAITING_FOR_COMPUTER = 4


PLAYER_TYPES = {
    0: PlayerTypes.HUMAN,
    1: PlayerTypes.RANDOM,
    2: PlayerTypes.RANDOM,
    None: PlayerTypes.TRICK_COMPLETE,
    -1: PlayerTypes.WAITING_FOR_COMPUTER,
}


class MenuOptions(Enum):
    MAIN_GAME = "Main Game"
    AI_GAME = "AI Game"
    TUTORIAL = "Tutorial"
    QUIT = "Quit"


class GameStage(Enum):
    BIDDING = 0
    PLAYING = 1
    DONE = 2


class Suit(int, Enum):
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
