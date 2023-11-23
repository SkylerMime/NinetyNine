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


def main(random_seed=None):
    player_types = PLAYER_TYPES

    print_welcome_message()

    game_state = game.GameState(random_seed)
    num_players = len(game_state.PLAYERS)

    print(f"The trump suit is: {game_state.TRUMP_SUIT}")

    for player_num in range(num_players):
        if player_types[player_num] == PlayerTypes.HUMAN:
            get_human_bid(game_state.PLAYERS[player_num])
        elif player_types[player_num] == PlayerTypes.RANDOM:
            get_random_bid(game_state.PLAYERS[player_num])

    final_state = play_one_hand_of_ninety_nine(game_state, player_types=player_types)

    print_line()
    print("The hand has ended")
    print("Scores:")
    scores = game.get_scores(final_state)
    print(f"Your Score: {scores[0]}")
    print(f"Player 1 Score: {scores[1]}")
    print(f"Player 2 Score: {scores[2]}")
    print_line()


def play_one_hand_of_ninety_nine(game_state, num_tricks=NUM_TRICKS, player_types=PLAYER_TYPES):
    next_to_play = 0

    for trick in range(num_tricks * NUM_PLAYERS):
        if player_types[next_to_play] == PlayerTypes.HUMAN:
            print("Your hand:")
            print_cards(game_state.PLAYERS[0].hand)
            print()
            card_to_play = get_human_card_play(next_to_play, game_state)
            print("You chose: ")
            print_card(card_to_play)
            print()
            game_state = game.make_card_play(game_state, next_to_play, card_to_play)
        elif player_types[next_to_play] == PlayerTypes.RANDOM:
            print(f"Player {next_to_play}'s move is: ")
            card_to_play = random.choice(
                list(game.get_legal_card_plays(game_state, next_to_play))
            )
            print_card(card_to_play)
            print()
            game_state = game.make_card_play(game_state, next_to_play, card_to_play)
        next_to_play = game_state.next_to_play
        if len(game_state.current_trick["cards"]) == 0:
            last_trick = game_state.trick_history[-1]
            trick_winner = game.get_trick_winner(last_trick, game_state.TRUMP_SUIT)
            print_trick_winner(trick_winner)

    return game_state


def all_cards_played(players: dict):
    for player in players.values():
        if len(player.hand) > 0:
            return False
    return True


def get_human_card_play(current_player_num, game_state):
    card_to_play = None
    while card_to_play not in game.get_legal_card_plays(game_state, current_player_num):
        print()
        print("Choose a card to play")
        card_to_play_string = input()
        card_to_play = get_valid_card(card_to_play_string)
    return card_to_play


def print_welcome_message():
    print_line()
    print("Welcome to Ninety Nine!\n")
    print_line()


def print_line():
    screen_width = 30
    for i in range(screen_width):
        print("#", end="")
    print("\n")


def get_human_bid(human: game.Player):
    while len(human.bid) < NUM_CARDS_IN_BID:
        print("Hand:")
        print_cards(human.hand)
        print()
        print("Bid:")
        print_cards(human.bid)
        print()
        print(
            "Choose a card to use in your bid ("
            + str(len(human.bid))
            + " out of "
            + str(NUM_CARDS_IN_BID)
            + ")"
        )
        next_bid_card_name = input()
        next_bid_card = get_valid_card(next_bid_card_name)
        if next_bid_card not in human.hand:
            print("That card is not in your hand")
        else:
            human.hand.remove(next_bid_card)
            human.bid.add(next_bid_card)


def get_random_bid(random_player: game.Player):
    for i in range(NUM_CARDS_IN_BID):
        next_bid_card = random.choice(list(random_player.hand))
        random_player.hand.remove(next_bid_card)
        random_player.bid.add(next_bid_card)


def get_valid_card(card_string: str) -> game.Card:
    card = game.Card(None, None)
    card_string = card_string.upper()
    match card_string[0]:
        case "A":
            card.rank = Rank.ACE
        case "K":
            card.rank = Rank.KING
        case "Q":
            card.rank = Rank.QUEEN
        case "J":
            card.rank = Rank.JACK
        case "T":
            card.rank = Rank.TEN
        case "9":
            card.rank = Rank.NINE
        case "8":
            card.rank = Rank.EIGHT
        case "7":
            card.rank = Rank.SEVEN
        case "6":
            card.rank = Rank.SIX
        case _:
            raise ValueError("Not a valid rank")

    match card_string[1]:
        case "D":
            card.suit = Suit.DIAMONDS
        case "S":
            card.suit = Suit.SPADES
        case "H":
            card.suit = Suit.HEARTS
        case "C":
            card.suit = Suit.CLUBS
        case _:
            raise ValueError("Not a valid suit")

    return card


def print_card(card: game.Card):
    print_rank(card.rank)
    print_suit(card.suit)


def print_rank(rank: Rank):
    match rank:
        case Rank.ACE:
            print("A", end="")
        case Rank.KING:
            print("K", end="")
        case Rank.QUEEN:
            print("Q", end="")
        case Rank.JACK:
            print("J", end="")
        case Rank.TEN:
            print("T", end="")
        case Rank.NINE:
            print("9", end="")
        case Rank.EIGHT:
            print("8", end="")
        case Rank.SEVEN:
            print("7", end="")
        case Rank.SIX:
            print("6", end="")
        case _:
            raise ValueError("Unknown rank")


def print_suit(suit: Suit):
    match suit:
        case Suit.DIAMONDS:
            print("D", end="")
        case Suit.SPADES:
            print("S", end="")
        case Suit.HEARTS:
            print("H", end="")
        case Suit.CLUBS:
            print("C", end="")
        case _:
            raise ValueError("Unknown suit")


def print_cards(cards: set):
    for card in get_sorted_cards(cards):
        print_card(card)
        print(" ", end="")


def get_sorted_cards(cards: set):
    cards = list(cards)
    cards.sort(reverse=True)
    return cards


def print_trick_winner(winner: int):
    if winner == 0:
        print("You won the trick")
    else:
        print(f"Player {winner} won the trick")


if __name__ == "__main__":
    main()
