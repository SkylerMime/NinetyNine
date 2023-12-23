import random

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

CARD_WIDTH = 131
CARD_HEIGHT = 186
CARD_INNER_BORDER = 5

BID_TOP = WINDOW_HEIGHT // 4
BID_LEFT = WINDOW_WIDTH // 2
HAND_TOP = WINDOW_HEIGHT - CARD_HEIGHT - 25
SPACE_BETWEEN_CARDS = WINDOW_WIDTH // 15
WIDTH_OF_FULL_HAND = (NUM_CARDS - 1) * SPACE_BETWEEN_CARDS + CARD_WIDTH
CARD_OUTSIDE_HORIZONTAL_MARGIN = WINDOW_WIDTH - WIDTH_OF_FULL_HAND
FULL_HAND_LEFT = CARD_OUTSIDE_HORIZONTAL_MARGIN // 2

BUTTON_WIDTH = 260
BUTTON_HEIGHT = 90
BUTTON_TOP = HAND_TOP - BUTTON_HEIGHT - 20
BUTTON_HORIZONTAL_CENTER = WINDOW_WIDTH // 2
BUTTON_LEFT = BUTTON_HORIZONTAL_CENTER - BUTTON_WIDTH // 2

TEXTVIEW_WIDTH = 360
TEXTVIEW_HEIGHT = 90
TEXTVIEW_TOP = 10
TEXTVIEW_LEFT = WINDOW_WIDTH - TEXTVIEW_WIDTH - 10

BID_MESSAGE_WIDTH = 90
BID_MESSAGE_HEIGHT = 90
BID_MESSAGE_TOP = 110
BID_MESSAGE_LEFT = WINDOW_WIDTH - BID_MESSAGE_WIDTH - 10

TRICKS_TAKEN_MESSAGE_WIDTH = 90
TRICKS_TAKEN_MESSAGE_HEIGHT = 90
TRICKS_TAKEN_MESSAGE_TOP = WINDOW_HEIGHT - TRICKS_TAKEN_MESSAGE_HEIGHT - 10
TRICKS_TAKEN_MESSAGE_LEFT = WINDOW_WIDTH - TRICKS_TAKEN_MESSAGE_WIDTH - 10

PRIMARY_TRICK_TOP = BID_TOP + 20
PRIMARY_TRICK_LEFT = WINDOW_WIDTH // 2 - CARD_WIDTH // 2

TRICK_POSITIONS = [
    pygame.Rect(PRIMARY_TRICK_LEFT, PRIMARY_TRICK_TOP, CARD_WIDTH, CARD_HEIGHT),
    pygame.Rect(
        PRIMARY_TRICK_LEFT - CARD_WIDTH - 40,
        PRIMARY_TRICK_TOP - CARD_HEIGHT,
        CARD_WIDTH,
        CARD_HEIGHT,
    ),
    pygame.Rect(
        PRIMARY_TRICK_LEFT + CARD_WIDTH + 40,
        PRIMARY_TRICK_TOP - CARD_HEIGHT,
        CARD_WIDTH,
        CARD_HEIGHT,
    ),
]

BLACK = (0, 0, 0)
GREEN = (0, 53, 24)
BLUE = (102, 178, 255)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = GREEN
BUTTON_COLOR = BLUE
BUTTON_TEXT_COLOR = WHITE
TEXTVIEW_COLOR = WHITE
TEXTVIEW_TEXT_COLOR = BLACK

MILLISECONDS_BETWEEN_PLAYS = 900


class TextView:
    def __init__(self):
        self.rect = pygame.Rect(
            TEXTVIEW_LEFT, TEXTVIEW_TOP, TEXTVIEW_WIDTH, TEXTVIEW_HEIGHT
        )
        self.bg_color = (TEXTVIEW_COLOR,)
        self.text_color = (TEXTVIEW_TEXT_COLOR,)
        self.message = "Hello World"
        self.rendered_text = None
        self.render_message()

    def render_message(self, message=None):
        if message is None:
            message = self.message
        else:
            self.message = message
        self.rendered_text = pygame.font.SysFont("Arial", 35).render(
            message, True, self.text_color, self.bg_color
        )


class Button(TextView):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(BUTTON_LEFT, BUTTON_TOP, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.bg_color = (BUTTON_COLOR,)
        self.text_color = (BUTTON_TEXT_COLOR,)
        self.message = "Confirm Bid"
        self.visible = False


class ClickableCard(Card):
    def __init__(self, rank: Rank, suit: Suit):
        super().__init__(rank, suit)
        self.card_image = None
        self.clickable_area = pygame.Rect(0, HAND_TOP, SPACE_BETWEEN_CARDS, CARD_HEIGHT)
        self.display_area = pygame.Rect(0, HAND_TOP, CARD_WIDTH, CARD_HEIGHT)

    def set_left(self, left):
        self.clickable_area.left = left
        self.display_area.left = left

    def set_top(self, top):
        self.clickable_area.top = top
        self.display_area.top = top

    def get_card(self):
        return Card(self.rank, self.suit)

    def __repr__(self):
        return f"""ClickableCard(rank={self.rank}, suit={self.suit},
        left={self.clickable_area.left}, top={self.clickable_area.top})"""

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

    while True:
        player_types = PLAYER_TYPES
        # display_welcome_message()
        images_dict = make_images_dict(game.get_all_cards())

        game_state = game.GameState()
        num_players = NUM_PLAYERS
        human_player: game.Player = game_state.PLAYERS[HUMAN_PLAYER_NUM]

        trump_message = TextView()
        trump_message.rect = pygame.Rect(
            TEXTVIEW_LEFT, TEXTVIEW_TOP, TEXTVIEW_WIDTH, TEXTVIEW_HEIGHT
        )
        trump_message.bg_color = TEXTVIEW_COLOR
        trump_message.text_color = TEXTVIEW_TEXT_COLOR
        trump_message.render_message(
            f"Trump Suit: {game_state.TRUMP_SUIT.name.capitalize()}"
        )

        bid_message = TextView()
        bid_message.rect = pygame.Rect(
            BID_MESSAGE_LEFT, BID_MESSAGE_TOP, BID_MESSAGE_WIDTH, BID_MESSAGE_HEIGHT
        )
        bid_message.bg_color = TEXTVIEW_COLOR
        bid_message.text_color = TEXTVIEW_TEXT_COLOR
        bid_message.render_message(f"{0}")

        tricks_taken_message = TextView()
        tricks_taken_message.rect = pygame.Rect(
            TRICKS_TAKEN_MESSAGE_LEFT,
            TRICKS_TAKEN_MESSAGE_TOP,
            TRICKS_TAKEN_MESSAGE_WIDTH,
            TRICKS_TAKEN_MESSAGE_HEIGHT,
        )
        tricks_taken_message.bg_color = TEXTVIEW_COLOR
        tricks_taken_message.text_color = TEXTVIEW_TEXT_COLOR
        tricks_taken_message.render_message(f"{0}")

        sorted_hand = game_display.get_sorted_cards(human_player.hand)
        clickable_hand = get_clickable_cards(sorted_hand, images_dict)
        clickable_bid = get_clickable_cards(list(human_player.bid), images_dict)

        for player_num in range(num_players):
            if player_types[player_num] == PlayerTypes.RANDOM:
                game_display.get_random_bid(game_state.PLAYERS[player_num])

        game_state, new_hand = do_bidding_loop(
            game_state,
            clickable_hand,
            clickable_bid,
            images_dict,
            screen,
            clock,
            trump_message,
            bid_message,
        )

        game_state = do_playing_loop(
            game_state,
            new_hand,
            images_dict,
            screen,
            clock,
            trump_message,
            bid_message,
            tricks_taken_message,
        )

        display_final_scores(screen, game_state, clock)


def do_bidding_loop(
    game_state,
    clickable_hand,
    clickable_bid,
    images_dict,
    screen,
    clock,
    trump_message,
    bid_message,
):
    continue_button = Button()
    continue_button.render_message("Confirm Bid")
    human_player = game_state.PLAYERS[HUMAN_PLAYER_NUM]
    while game_state.stage == GameStage.BIDDING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_card = get_card_from_click(
                    event.pos, clickable_hand + clickable_bid
                )
                if clicked_card in clickable_hand:
                    human_player.hand.remove(clicked_card.get_card())
                    human_player.bid.add(clicked_card.get_card())
                if clicked_card in clickable_bid:
                    human_player.bid.remove(clicked_card.get_card())
                    human_player.hand.add(clicked_card.get_card())
                if clicked_card:
                    sorted_hand = game_display.get_sorted_cards(human_player.hand)
                    clickable_hand = get_clickable_cards(sorted_hand, images_dict)
                    clickable_bid = get_clickable_cards(
                        list(human_player.bid), images_dict
                    )
                    new_bid_amount = game.bid_value(clickable_bid)
                    bid_message.render_message(f"{new_bid_amount}")
                    center_cards(clickable_hand)
                    center_cards(clickable_bid, BID_TOP)

                if continue_button.visible and continue_button.rect.collidepoint(
                    event.pos
                ):
                    game_state.stage = GameStage.PLAYING
                    continue_button.visible = False

        if len(human_player.bid) == 3:
            continue_button.visible = True
        else:
            continue_button.visible = False

        screen.fill(BACKGROUND_COLOR)
        draw_clickable_cards(screen, clickable_hand)
        draw_clickable_cards(screen, clickable_bid)
        if trump_message:
            draw_message(screen, trump_message)
        if bid_message:
            draw_message(screen, bid_message)
        if continue_button.visible:
            draw_button(screen, continue_button)

        pygame.display.flip()
        clock.tick(60)

    return game_state, clickable_hand


def do_playing_loop(
    game_state,
    clickable_hand,
    images_dict,
    screen,
    clock: pygame.time.Clock,
    trump_message=None,
    bid_message=None,
    tricks_taken_message=None,
    player_types=PLAYER_TYPES,
    human_player_num=HUMAN_PLAYER_NUM,
):
    continue_button = Button()
    continue_button.render_message("Next trick")
    continue_button.visible = False
    center_cards(clickable_hand)
    time_of_next_play = pygame.time.get_ticks() + MILLISECONDS_BETWEEN_PLAYS
    while game_state.stage == GameStage.PLAYING:
        if (
            pygame.time.get_ticks() > time_of_next_play
            and game_state.next_to_play == -1
        ):
            # The player has just finished their turn
            game_state.next_to_play = 1
        # process player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_card = get_card_from_click(event.pos, clickable_hand)
                if (
                    game_state.next_to_play == HUMAN_PLAYER_NUM
                    and clicked_card
                    and clicked_card.get_card()
                    in game.get_legal_card_plays(game_state, HUMAN_PLAYER_NUM)
                ):
                    game_state = game.make_card_play(
                        game_state, HUMAN_PLAYER_NUM, clicked_card.get_card()
                    )
                    sorted_hand = game_display.get_sorted_cards(
                        game_state.PLAYERS[human_player_num].hand
                    )
                    clickable_hand = get_clickable_cards(sorted_hand, images_dict)
                    center_cards(clickable_hand)
                    time_of_next_play = (
                        pygame.time.get_ticks() + MILLISECONDS_BETWEEN_PLAYS
                    )
                if continue_button.visible and continue_button.rect.collidepoint(
                    event.pos
                ):
                    game_state = game.finish_trick(game_state)
                    continue_button.visible = False

        # logical updates here
        if (
            player_types[game_state.next_to_play] == PlayerTypes.RANDOM
            and pygame.time.get_ticks() > time_of_next_play
        ):
            card_to_play = random.choice(
                list(game.get_legal_card_plays(game_state, game_state.next_to_play))
            )
            game_state = game.make_card_play(
                game_state, game_state.next_to_play, card_to_play
            )
            time_of_next_play = pygame.time.get_ticks() + MILLISECONDS_BETWEEN_PLAYS

        continue_button.visible = game.is_full(game_state.current_trick)

        if (
            game.game_is_over(game_state)
            and pygame.time.get_ticks() > time_of_next_play
        ):
            game_state.stage = GameStage.DONE

        if tricks_taken_message:
            tricks_taken = game_state.PLAYERS[HUMAN_PLAYER_NUM].tricks_won
            tricks_taken_message.render_message(f"{tricks_taken}")

        # render graphics here
        screen.fill(BACKGROUND_COLOR)
        draw_clickable_cards(screen, clickable_hand)
        draw_trick(screen, game_state.current_trick, images_dict)
        if trump_message:
            draw_message(screen, trump_message)
        if bid_message:
            draw_message(screen, bid_message)
        if tricks_taken_message:
            draw_message(screen, tricks_taken_message)

        if continue_button.visible:
            draw_button(screen, continue_button)

        pygame.display.flip()
        clock.tick(60)

    return game_state


def display_final_scores(screen, final_state, clock):
    final_scores = game.get_scores(final_state)
    continue_button = Button()
    continue_button.render_message("Start new game")
    continue_button.visible = True
    continue_button.rect.top += 80
    while final_state.stage == GameStage.DONE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                if continue_button.visible and continue_button.rect.collidepoint(
                    event.pos
                ):
                    final_state.stage = GameStage.BIDDING
                    continue_button.visible = False

        screen.fill(BACKGROUND_COLOR)
        score_bg_rect = pygame.Rect(0, 0, 600, 200)
        score_bg_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
        pygame.draw.rect(screen, TEXTVIEW_COLOR, score_bg_rect)
        scores_message = TextView()
        scores_message.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 55)
        scores_message.render_message(f"   Your score: {final_scores[0]}   ")
        screen.blit(scores_message.rendered_text, scores_message.rect)
        scores_message = TextView()
        scores_message.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10)
        scores_message.render_message(f"   Opponent 1: {final_scores[1]}   ")
        screen.blit(scores_message.rendered_text, scores_message.rect)
        scores_message = TextView()
        scores_message.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 35)
        scores_message.render_message(f"   Opponent 2: {final_scores[2]}   ")
        screen.blit(scores_message.rendered_text, scores_message.rect)

        if continue_button.visible:
            draw_button(screen, continue_button)

        pygame.display.flip()
        clock.tick(60)


def draw_trick(
    screen: pygame.Surface,
    trick: game.Trick,
    images_dict,
    trick_positions=None,
):
    if trick_positions is None:
        trick_positions = TRICK_POSITIONS
    cards: dict = trick.cards
    for player, card in cards.items():
        card_image = images_dict[card.suit.name.lower()][card.rank.name.lower()]
        screen.blit(card_image, trick_positions[player])


def draw_button(screen: pygame.Surface, button: Button):
    pygame.draw.rect(screen, button.bg_color, button.rect)
    text_rect = button.rendered_text.get_rect(center=button.rect.center)
    screen.blit(button.rendered_text, text_rect)


def draw_message(screen: pygame.Surface, message: TextView):
    pygame.draw.rect(screen, message.bg_color, message.rect)
    text_rect = message.rendered_text.get_rect(center=message.rect.center)
    screen.blit(message.rendered_text, text_rect)


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
    for card_num, card in enumerate(cards):
        clickable_card = ClickableCard(card.rank, card.suit)
        clickable_card.card_image = image_dict[card.suit.name.lower()][
            card.rank.name.lower()
        ]
        clickable_card.set_left(FULL_HAND_LEFT + card_num * SPACE_BETWEEN_CARDS)
        clickable_cards.append(clickable_card)
    return clickable_cards


def center_cards(
    cards_to_center: list[ClickableCard],
    first_card_y: int = HAND_TOP,
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
    for card in hand_cards:
        screen.blit(
            card.card_image,
            card.display_area,
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
