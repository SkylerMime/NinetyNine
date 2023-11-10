"""
Connect 4 game
For use of experimenting with Monte Carlo Search Trees
"""

# Constants
NUM_COLUMNS = 7
NUM_ROWS = 6
PLAYERS = {"none": 0, "one": 1, "two": 2}
OUTCOMES = {"none": 0, "one": 1, "two": 2, "draw": 3}
type Board = list[list[str]]


class ConnectFourState:
    def __init__(self):
        self.board = create_board()
        self.to_play = PLAYERS["one"]


def copy_state(state: ConnectFourState) -> ConnectFourState:
    state.board = copy_board(state.board)
    return state


# Return a 6x7 board with X or O for the two players and _ representing no piece, [0][0] is the top-left coordinate
def create_board() -> Board:
    board = []
    for row in range(NUM_ROWS):
        board.append([])
        for col in range(NUM_COLUMNS):
            board[row].append("_")
    return board


# Print out the current board
def print_board(board: Board):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS):
            if board[row][col] == PLAYERS["one"]:
                print("X", end="")
            elif board[row][col] == PLAYERS["two"]:
                print("O", end="")
            else:
                print("_", end="")
        print()  # newline
    print("0123456")


def copy_board(board: Board):
    # Uses list slicing to make a deep copy of the board
    return [col[:] for col in board]


# Return a new board with the given move
def make_move_to_board(player: int, column: int, board: Board):
    new_board = copy_board(board)
    if column >= NUM_COLUMNS:
        raise ValueError("column must be less than the number of columns")
    if new_board[0][column] != "_":
        raise ValueError("illegal move: column is full")

    # if this column is empty, add this piece to the bottom
    if new_board[NUM_ROWS - 1][column] == "_":
        new_board[NUM_ROWS - 1][column] = player
    # otherwise, find where this piece should drop to
    else:
        for row in range(NUM_ROWS):
            if new_board[row][column] != "_":
                # we have found the first non-empty space
                new_board[row - 1][column] = player
                break
    return new_board


def make_move(column: int, state: ConnectFourState):
    new_state = ConnectFourState()
    new_state.to_play = next_player(state.to_play)
    new_state.board = make_move_to_board(state.to_play, column, state.board)
    return new_state


def next_player(current_player: int):
    if current_player == PLAYERS["one"]:
        return PLAYERS["two"]
    else:
        return PLAYERS["one"]


# Return true if the given player has won
def has_won(player: int, board: Board) -> bool:
    # Check each horizontal for a four-in-a-row
    for row in board:
        for columnNum in range(NUM_COLUMNS - 3):
            if (
                row[columnNum] == player
                and row[columnNum + 1] == player
                and row[columnNum + 2] == player
                and row[columnNum + 3] == player
            ):
                return True

    # Check each vertical
    for columnNum in range(NUM_COLUMNS):
        for rowNum in range(NUM_ROWS - 3):
            if (
                board[rowNum][columnNum] == player
                and board[rowNum + 1][columnNum] == player
                and board[rowNum + 2][columnNum] == player
                and board[rowNum + 3][columnNum] == player
            ):
                return True

    # Check each positive-slope diagonal starting at each column, starting with "3" and ending with the last row
    for columnNum in range(NUM_COLUMNS - 4):
        for startingRowNum in range(3, NUM_ROWS):
            if (
                board[startingRowNum][columnNum] == player
                and board[startingRowNum - 1][columnNum + 1] == player
                and board[startingRowNum - 2][columnNum + 2] == player
                and board[startingRowNum - 3][columnNum + 3] == player
            ):
                return True

    # Check each negative-slope diagonal starting at each column, starting with "0" and ending with the nth - 4 row
    for columnNum in range(NUM_COLUMNS - 4):
        for startingRowNum in range(0, NUM_ROWS - 4):
            if (
                board[startingRowNum][columnNum] == player
                and board[startingRowNum + 1][columnNum + 1] == player
                and board[startingRowNum + 2][columnNum + 2] == player
                and board[startingRowNum + 3][columnNum + 3] == player
            ):
                return True

    # If no win is found...
    return False


def is_a_draw(board: Board) -> bool:
    for columnNum in range(NUM_COLUMNS):
        if board[0][columnNum] == "_":
            return False
    if has_won(PLAYERS["one"], board) or has_won(PLAYERS["two"], board):
        return False
    return True


def get_legal_moves(state: ConnectFourState):
    return [col for col in range(NUM_COLUMNS) if state.board[0][col] == 0]


def is_over(state: ConnectFourState) -> bool:
    if (
        has_won(PLAYERS["one"], state.board)
        or has_won(PLAYERS["two"], state.board)
        or is_a_draw(state.board)
    ):
        return True
    return False


def get_winner(state: ConnectFourState) -> int or None:
    if is_a_draw(state.board):
        return OUTCOMES["draw"]

    if has_won(PLAYERS["one"], state.board):
        return OUTCOMES["one"]
    if has_won(PLAYERS["two"], state.board):
        return OUTCOMES["two"]

    return None
