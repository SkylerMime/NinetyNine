import pygame
from ninety_nine import ninety_nine_state as game
from ninety_nine import human_ai_main_game as game_display
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

HUMAN_PLAYER_NUM = 0

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

CARD_WIDTH = 655 / 5
CARD_HEIGHT = 930 / 5
CARD_INNER_BORDER = 5

CARD_Y_POSITION = WINDOW_HEIGHT * 3 // 5
SPACE_BETWEEN_CARDS = WINDOW_WIDTH // 15

GREEN = (0, 53, 24)
BACKGROUND_COLOR = GREEN


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Ninety Nine")
    clock = pygame.time.Clock()

    player_types = PLAYER_TYPES
    # display_welcome_message()

    game_state = game.GameState()
    num_players = NUM_PLAYERS
    human_player: game.Player = game_state.PLAYERS[HUMAN_PLAYER_NUM]

    for player_num in range(num_players):
        if player_types[player_num] == PlayerTypes.RANDOM:
            game_display.get_random_bid(game_state.PLAYERS[player_num])

    while True:
        # process player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # logical updates here

        screen.fill(BACKGROUND_COLOR)
        sorted_hand = game_display.get_sorted_cards(human_player.hand)
        hand_images = get_images_from_cards(sorted_hand)
        draw_hand(screen, hand_images, 50)
        # display_trump_suit_in_top_right_corner()

        # render graphics here

        pygame.display.flip()
        clock.tick(60)


def draw_hand(
    screen: pygame.Surface,
    hand_images: list,
    first_card_x: int,
    first_card_y: int = CARD_Y_POSITION,
    x_margin: int = SPACE_BETWEEN_CARDS,
):
    for card_num in range(len(hand_images)):
        screen.blit(
            hand_images[card_num], (first_card_x + card_num * x_margin, first_card_y)
        )


def get_images_from_cards(cards: list):
    images = []
    for card in cards:
        images.append(get_image_from_card(card))
    return images


def get_image_from_card(
    card: game.Card, width: int = CARD_WIDTH, height: int = CARD_HEIGHT, border: int = CARD_INNER_BORDER
):
    image_filename = get_image_filename_from_card(card)
    raw_image = pygame.image.load(image_filename).convert()
    shrunk_image = pygame.transform.scale(raw_image, (width - 2*border, height - 2*border))
    border_surface = pygame.Surface((width, height))
    border_surface.fill('black')
    border_surface.blit(shrunk_image, (border, border))
    return border_surface


def get_image_filename_from_card(card: game.Card):
    image_rank = str(card.rank.name).lower()
    match image_rank:
        case "ten":
            image_rank = "10"
        case "nine":
            image_rank = "9"
        case "eight":
            image_rank = "8"
        case "seven":
            image_rank = "7"
        case "six":
            image_rank = "6"
    image_suit = str(card.suit.name).lower()
    return f"card_images/{image_suit}_{image_rank}.png"


if __name__ == "__main__":
    main()
