import monte_carlo_search_tree as mcst
import connect_four as game
from connect_four import Board

PLAYER_SYM = "X"
COMPUTER_SYM = "O"


def get_player_move():
    print("Select a column to drop in, 0-" + str(game.NUM_COLUMNS - 1))
    player_input_valid = False
    while not player_input_valid:
        player_input = input()
        if (
                player_input.isdigit()
                and 0 <= int(player_input) < game.NUM_COLUMNS
        ):
            player_input_valid = True
        else:
            print(
                "Invalid input. Expected number between 0 and "
                + str(game.NUM_COLUMNS - 1)
            )
    return int(player_input)


def get_computer_move(root_state: mcst.ConnectFourNode):
    return mcst.monte_carlo_tree_search(root_state).parentColumnDroppedIn


def main():
    print(
        "Welcome to Four in a Row! You will make the first move as '" + PLAYER_SYM + "'"
    )
    winner = None
    current_board = game.new_board()
    game.print_board(current_board)
    while True:
        player_move = get_player_move()
        current_board = game.make_move(PLAYER_SYM, player_move, current_board)
        game.print_board(current_board)
        current_game_state = mcst.ConnectFourNode(
            None, current_board, player_move, PLAYER_SYM
        )
        if game.has_won(PLAYER_SYM, current_board):
            winner = PLAYER_SYM
            break

        computer_move = get_computer_move(current_game_state)
        current_board = game.make_move(COMPUTER_SYM, computer_move, current_board)
        game.print_board(current_board)
        if game.has_won(COMPUTER_SYM, current_board):
            winner = COMPUTER_SYM
            break

    print("The " + winner + " has won! Play again?")


if __name__ == "__main__":
    main()
