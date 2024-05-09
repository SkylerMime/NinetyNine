import math
import random
from dataclasses import dataclass
from typing import Self

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
    MenuOptions,
)
from ninety_nine.monte_carlo_tree_search import NinetyNineMCST

IMAGES_DIRECTORY_PATH = (
    "ninety_nine/card_images"
)

NUM_CARDS = NUM_CARDS_IN_BID + NUM_TRICKS

AI_PLAYER_COMBINATION = {
    0: PlayerTypes.HUMAN,
    1: PlayerTypes.MONTE_CARLO_AI,
    2: PlayerTypes.RANDOM,
    None: PlayerTypes.TRICK_COMPLETE,
    -1: PlayerTypes.WAITING_FOR_COMPUTER,
}

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

SPACE_BETWEEN_MENU_BUTTONS = 20
NUM_OPTIONS = len(MenuOptions)
WIDTH_OF_FULL_MENU = (BUTTON_WIDTH + SPACE_BETWEEN_MENU_BUTTONS - 1) * NUM_OPTIONS
MENU_LEFT_START = BUTTON_HORIZONTAL_CENTER - (WIDTH_OF_FULL_MENU // 2)

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


@dataclass
class CardVector:
    x: float
    y: float

    def __add__(self, vector: Self):
        return CardVector(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector: Self):
        return CardVector(self.x - vector.x, self.y - vector.y)

    def __truediv__(self, other: float):
        return CardVector(self.x / other, self.y / other)

    def __eq__(self, vector):
        delta = 0.01
        if isinstance(vector, CardVector):
            return abs(self.x - vector.x) < delta and abs(self.y - vector.y) < delta
        else:
            return False


TRICK_INITIAL_POSITIONS = [
    None,
    CardVector(0, PRIMARY_TRICK_TOP - CARD_HEIGHT),
    CardVector(WINDOW_WIDTH, PRIMARY_TRICK_TOP - CARD_HEIGHT),
]
TRICK_FINAL_POSITIONS = [
    CardVector(PRIMARY_TRICK_LEFT, PRIMARY_TRICK_TOP),
    CardVector(
        PRIMARY_TRICK_LEFT - CARD_WIDTH - 40,
        PRIMARY_TRICK_TOP - CARD_HEIGHT / 2,
    ),
    CardVector(
        PRIMARY_TRICK_LEFT + CARD_WIDTH + 40,
        PRIMARY_TRICK_TOP - CARD_HEIGHT / 2,
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
# If this number is too high, the system could crash
FRAMES_PER_SECOND = 120


class TextView:
    def __init__(self):
        self.rect = pygame.Rect(
            TEXTVIEW_LEFT, TEXTVIEW_TOP, TEXTVIEW_WIDTH, TEXTVIEW_HEIGHT
        )
        self.bg_color = TEXTVIEW_COLOR
        self.text_color = TEXTVIEW_TEXT_COLOR
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
        self.menu_option: MenuOptions | None = None


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
        selected_menu_option = None
        buttons = []
        for option_num, menu_option in enumerate(MenuOptions):
            menu_string = menu_option.value
            new_button = Button()
            new_button.rect.left = (
                MENU_LEFT_START
                + (BUTTON_WIDTH + SPACE_BETWEEN_MENU_BUTTONS) * option_num
            )
            new_button.render_message(menu_string)
            new_button.menu_option = menu_option
            buttons.append(new_button)

        while not selected_menu_option:
            selected_menu_option = get_clicked_menu_option(buttons)
            # graphics
            draw_menu(screen, buttons)
            clock.tick(FRAMES_PER_SECOND)

        player_types = PLAYER_TYPES
        match selected_menu_option:
            case MenuOptions.MAIN_GAME:
                player_types = PLAYER_TYPES
            case MenuOptions.AI_GAME:
                player_types = AI_PLAYER_COMBINATION
            case MenuOptions.QUIT:
                pygame.quit()
                raise SystemExit
            case _:
                raise SystemExit("Invalid menu option")

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
            if player_types[player_num] in {
                PlayerTypes.RANDOM,
                PlayerTypes.MONTE_CARLO_AI,
            }:
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

        if PlayerTypes.MONTE_CARLO_AI in player_types.values():
            mcst = NinetyNineMCST(game_state)
        else:
            mcst = None

        game_state = do_playing_loop(
            game_state,
            new_hand,
            images_dict,
            screen,
            clock,
            trump_message,
            bid_message,
            tricks_taken_message,
            player_types=player_types,
            mcst=mcst,
        )

        display_final_scores(screen, game_state, clock)


def get_clicked_menu_option(buttons: list[Button]):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    return button.menu_option
    return None


def draw_menu(screen, buttons):
    screen.fill(BACKGROUND_COLOR)
    for button in buttons:
        draw_button(screen, button)
    pygame.display.flip()


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
                if clicked_card in clickable_hand and not continue_button.visible:
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
        clock.tick(FRAMES_PER_SECOND)

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
    mcst=None,
):
    continue_button = Button()
    continue_button.render_message("Next trick")
    continue_button.visible = False
    center_cards(clickable_hand)
    time_of_next_play = pygame.time.get_ticks() + MILLISECONDS_BETWEEN_PLAYS
    current_trick_positions: list[None | CardVector] = [None] * 3
    current_trick_vectors: list[None | CardVector] = [None] * 3
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
                card_to_play = None
                clicked_card = get_card_from_click(event.pos, clickable_hand)
                if clicked_card:
                    card_to_play = clicked_card.get_card()
                if (
                    game_state.next_to_play == HUMAN_PLAYER_NUM
                    and card_to_play
                    in game.get_legal_card_plays(game_state, HUMAN_PLAYER_NUM)
                ):
                    game_state = game.make_card_play(
                        game_state, HUMAN_PLAYER_NUM, card_to_play
                    )
                    if mcst:
                        mcst.play_card(card_to_play)
                    sorted_hand = game_display.get_sorted_cards(
                        game_state.PLAYERS[human_player_num].hand
                    )
                    clickable_hand = get_clickable_cards(sorted_hand, images_dict)
                    center_cards(clickable_hand)
                    current_trick_positions[
                        HUMAN_PLAYER_NUM
                    ] = CardVector(clicked_card.display_area.x, clicked_card.display_area.y)
                    current_trick_vectors[
                        HUMAN_PLAYER_NUM
                    ] = get_movement_vector_toward(
                        current_trick_positions[HUMAN_PLAYER_NUM],
                        TRICK_FINAL_POSITIONS[HUMAN_PLAYER_NUM],
                    )
                    time_of_next_play = (
                        pygame.time.get_ticks() + MILLISECONDS_BETWEEN_PLAYS
                    )
                if continue_button.visible and continue_button.rect.collidepoint(
                    event.pos
                ):
                    game_state = game.finish_trick(game_state)
                    current_trick_positions = [None] * 3
                    continue_button.visible = False

        # logical updates here
        if (
            player_types[game_state.next_to_play] == PlayerTypes.RANDOM
            and pygame.time.get_ticks() > time_of_next_play
        ):
            card_to_play = get_random_card_to_play(game_state)
            current_trick_positions[game_state.next_to_play] = TRICK_INITIAL_POSITIONS[
                game_state.next_to_play
            ]
            current_trick_vectors[game_state.next_to_play] = get_movement_vector_toward(
                current_trick_positions[game_state.next_to_play],
                TRICK_FINAL_POSITIONS[game_state.next_to_play],
            )
            game_state = game.make_card_play(
                game_state, game_state.next_to_play, card_to_play
            )
            if mcst:
                mcst.play_card(card_to_play)
            time_of_next_play = pygame.time.get_ticks() + MILLISECONDS_BETWEEN_PLAYS

        elif (
            player_types[game_state.next_to_play] == PlayerTypes.MONTE_CARLO_AI
            and pygame.time.get_ticks() > time_of_next_play
        ):
            mcst.search(1)
            card_to_play = mcst.best_move()
            mcst.play_card(card_to_play)
            current_trick_positions[game_state.next_to_play] = TRICK_INITIAL_POSITIONS[
                game_state.next_to_play
            ]
            current_trick_vectors[game_state.next_to_play] = get_movement_vector_toward(
                current_trick_positions[game_state.next_to_play],
                TRICK_FINAL_POSITIONS[game_state.next_to_play],
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
            continue_button.render_message(
                "See scores"
            )  # TODO: Why doesn't this show in the game?

        if tricks_taken_message:
            tricks_taken = game_state.PLAYERS[HUMAN_PLAYER_NUM].tricks_won
            tricks_taken_message.render_message(f"{tricks_taken}")

        # render graphics here
        screen.fill(BACKGROUND_COLOR)
        draw_clickable_cards(screen, clickable_hand)
        current_trick_positions = get_new_card_positions(
            current_trick_positions, TRICK_FINAL_POSITIONS, current_trick_vectors
        )
        draw_trick(
            screen, game_state.current_trick, images_dict, current_trick_positions
        )
        if trump_message:
            draw_message(screen, trump_message)
        if bid_message:
            draw_message(screen, bid_message)
        if tricks_taken_message:
            draw_message(screen, tricks_taken_message)

        if continue_button.visible:
            draw_button(screen, continue_button)

        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)

    return game_state


def get_random_card_to_play(game_state):
    return random.choice(
        list(game.get_legal_card_plays(game_state, game_state.next_to_play))
    )


def display_final_scores(screen, final_state, clock):
    final_scores = game.get_scores(final_state)
    continue_button = Button()
    continue_button.render_message("Menu")
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
        clock.tick(FRAMES_PER_SECOND)


def get_movement_vector_toward(
    initial_pos: CardVector, final_pos: CardVector, ticks_to_reach = 100
):
    tip_to_tail: CardVector = final_pos - initial_pos
    return tip_to_tail / ticks_to_reach


def magnitude(vector: CardVector):
    return math.sqrt(vector.x ** 2 + vector.y ** 2)


def get_new_card_positions(
    current_positions: list[CardVector],
    end_positions: list[CardVector],
    vectors: list[CardVector],
):
    assert len(current_positions) == len(end_positions) == len(vectors)
    new_positions = [None]*len(current_positions)
    for player, pos in enumerate(current_positions):
        if pos is not None:
            final_pos: CardVector = end_positions[player]
            # if the rect is within "speed" of its destination, move it there
            if magnitude(final_pos - pos) < magnitude(vectors[player]):
                new_positions[player] = final_pos
            else:
                new_positions[player] = current_positions[player] + vectors[player]
    return new_positions


def draw_trick(
    screen: pygame.Surface,
    trick: game.Trick,
    images_dict,
    trick_positions=None,
):
    if trick_positions is None:
        trick_positions = TRICK_FINAL_POSITIONS
    cards: dict = trick.cards
    for player, card in cards.items():
        card_image = images_dict[card.suit.name.lower()][card.rank.name.lower()]
        screen.blit(card_image, (trick_positions[player].x, trick_positions[player].y, CARD_WIDTH, CARD_HEIGHT))


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
    return f"{IMAGES_DIRECTORY_PATH}/{image_suit}_{image_rank}.svg"


if __name__ == "__main__":
    main()
