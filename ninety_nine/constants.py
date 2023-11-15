from enum import Enum


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
