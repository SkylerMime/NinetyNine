import pygame
from ninety_nine import ninety_nine_state as game
from ninety_nine import human_ai_main_game as game_display
from ninety_nine.ninety_nine_state import Card
from ninety_nine.constants import (
    PlayerTypes,
    Rank,
    Suit,
    GameStage,
    NUM_CARDS_IN_BID,
    PLAYER_TYPES,
    NUM_TRICKS,
    NUM_PLAYERS,
)

IMAGES_DIRECTORY_PATH = (
    "/Users/Skyler/Coding/PythonPrograms/NinetyNine/ninety_nine/card_images"
)

NUM_CARDS = NUM_CARDS_IN_BID + NUM_TRICKS

HUMAN_PLAYER_NUM = 0

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

CARD_WIDTH = 655 // 5
CARD_HEIGHT = 930 // 5
CARD_INNER_BORDER = 5

BID_Y_POSITION = WINDOW_HEIGHT // 4
BID_X_POSITION = WINDOW_WIDTH // 2
HAND_Y_POSITION = WINDOW_HEIGHT - CARD_HEIGHT - 25
SPACE_BETWEEN_CARDS = WINDOW_WIDTH // 15
WIDTH_OF_FULL_HAND = (NUM_CARDS - 1) * SPACE_BETWEEN_CARDS + CARD_WIDTH
CARD_OUTSIDE_HORIZONTAL_MARGIN = WINDOW_WIDTH - WIDTH_OF_FULL_HAND
HAND_X_POSITION = CARD_OUTSIDE_HORIZONTAL_MARGIN // 2

GREEN = (0, 53, 24)
BACKGROUND_COLOR = GREEN


class ClickableCard(Card):
    def __init__(self, rank: Rank, suit: Suit):
        super().__init__(rank, suit)
        self.card_image = None
        self.clickable_area = pygame.Rect(
            0, HAND_Y_POSITION, SPACE_BETWEEN_CARDS, CARD_HEIGHT
        )
        self.display_area = pygame.Rect(0, HAND_Y_POSITION, CARD_WIDTH, CARD_HEIGHT)

    def set_left(self, left):
        self.clickable_area.left = left
        self.display_area.left = left

    def set_top(self, top):
        self.clickable_area.top = top
        self.display_area.top = top

    def get_card(self):
        return Card(self.rank, self.suit)

    def __eq__(self, other):
        if isinstance(other, ClickableCard):
            return (
                super().__eq__(other)
                and self.clickable_area == other.clickable_area
                and self.display_area == other.display_area
            )
        return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Ninety Nine")
    clock = pygame.time.Clock()

    player_types = PLAYER_TYPES
    # display_welcome_message()
    images_dict = make_images_dict(game.get_all_cards())

    game_state = game.GameState()
    num_players = NUM_PLAYERS
    human_player: game.Player = game_state.PLAYERS[HUMAN_PLAYER_NUM]

    sorted_hand = game_display.get_sorted_cards(human_player.hand)
    clickable_hand = get_clickable_cards(sorted_hand, images_dict)
    clickable_bid = get_clickable_cards(list(human_player.bid), images_dict)

    for player_num in range(num_players):
        if player_types[player_num] == PlayerTypes.RANDOM:
            game_display.get_random_bid(game_state.PLAYERS[player_num])

    while game_state.stage == GameStage.BIDDING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_card = get_card_from_click(event.pos, clickable_hand)
                if clicked_card:
                    human_player.hand.remove(clicked_card.get_card())
                    human_player.bid.add(clicked_card.get_card())
                    sorted_hand = game_display.get_sorted_cards(human_player.hand)
                    clickable_hand = get_clickable_cards(sorted_hand, images_dict)
                    clickable_bid = get_clickable_cards(
                        list(human_player.bid), images_dict
                    )
                    center_cards(clickable_hand)
                    center_cards(clickable_bid, BID_Y_POSITION)

        if len(human_player.bid) == 3:
            game_state.stage = GameStage.PLAYING

        screen.fill(BACKGROUND_COLOR)
        draw_clickable_cards(screen, clickable_hand)
        draw_clickable_cards(screen, clickable_bid)
        # display_trump_suit_in_top_right_corner()

        pygame.display.flip()
        clock.tick(60)

    pygame.time.wait(2000)

    while game_state.stage == GameStage.PLAYING:
        # process player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_card = get_card_from_click(event.pos, clickable_hand)
                if clicked_card:
                    pass

        # logical updates here

        screen.fill(BACKGROUND_COLOR)
        sorted_hand = game_display.get_sorted_cards(human_player.hand)
        clickable_hand = get_clickable_cards(sorted_hand, images_dict)
        draw_clickable_cards(screen, clickable_hand)
        # display_trump_suit_in_top_right_corner()

        # render graphics here

        pygame.display.flip()
        clock.tick(60)


def get_card_from_click(pos, all_cards: list[ClickableCard]):
    for card in all_cards:
        if card.clickable_area.collidepoint(pos):
            return card
    return None


def make_images_dict(cards):
    images_dict = {}
    # make outer dictionary of suits
    for card in cards:
        images_dict[card.suit.name.lower()] = {}
    # fill inner dictionaries of ranks
    for card in cards:
        images_dict[card.suit.name.lower()][
            card.rank.name.lower()
        ] = load_bordered_image_of_card(card)
    return images_dict


def get_clickable_cards(cards: list, image_dict: dict):
    clickable_cards = []
    for card_num in range(len(cards)):
        card = cards[card_num]
        clickable_card = ClickableCard(card.rank, card.suit)
        clickable_card.card_image = image_dict[card.suit.name.lower()][
            card.rank.name.lower()
        ]
        clickable_card.set_left(HAND_X_POSITION + card_num * SPACE_BETWEEN_CARDS)
        clickable_cards.append(clickable_card)
    return clickable_cards


def center_cards(
    cards_to_center: list[ClickableCard],
    first_card_y: int = HAND_Y_POSITION,
    x_margin: int = SPACE_BETWEEN_CARDS,
    card_width: int = CARD_WIDTH,
    card_height: int = CARD_HEIGHT,
):
    num_cards = len(cards_to_center)
    spread_width = (num_cards - 1) * x_margin + card_width
    first_card_x = (WINDOW_WIDTH - spread_width) / 2
    for card_num in range(num_cards):
        card_left = first_card_x + card_num * x_margin
        card_top = first_card_y
        cards_to_center[card_num].clickable_area = pygame.Rect(
            card_left, card_top, x_margin, card_height
        )
        cards_to_center[card_num].display_area = pygame.Rect(
            card_left, card_top, card_width, card_height
        )


def draw_clickable_cards(
    screen: pygame.Surface,
    hand_cards: list[ClickableCard],
):
    num_cards = len(hand_cards)
    for card_num in range(num_cards):
        screen.blit(
            hand_cards[card_num].card_image,
            hand_cards[card_num].display_area,
        )


def get_images_from_cards(cards: list, image_dict: dict):
    images = []
    for card in cards:
        images.append(image_dict[card.suit.name.lower()][card.rank.name.lower()])
    return images


def load_bordered_image_of_card(
    card: game.Card,
    width: int = CARD_WIDTH,
    height: int = CARD_HEIGHT,
    border: int = CARD_INNER_BORDER,
):
    image_filename = get_image_filename_from_card(card)
    raw_image = pygame.image.load(image_filename)
    shrunk_image = pygame.transform.scale(
        raw_image, (width - 2 * border, height - 2 * border)
    )
    border_surface = pygame.Surface((width, height))
    border_surface.fill("black")
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
    return f"{IMAGES_DIRECTORY_PATH}/{image_suit}_{image_rank}.png"


if __name__ == "__main__":
    main()
