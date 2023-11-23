import pygame
from ninety_nine import ninety_nine_state as game
import random
from ninety_nine.constants import (
    PlayerTypes,
    Rank,
    Suit,
    NUM_CARDS_IN_BID,
    PLAYER_TYPES,
    NUM_TRICKS,
    NUM_PLAYERS,
)


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    while True:
        # process player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # logical updates here

        screen.fill("green")

        # render graphics here

        pygame.display.flip()
        clock.tick(60)


def draw_hand(hand: list, first_card_x: int, first_card_y: int):
    for card in hand:
        pass


def get_image_from_card(card: game.Card):




if __name__ == '__main__':
    main()