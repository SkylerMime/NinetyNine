'''
Connect 4 game
For use of experimenting with Monte Carlo Search Trees
'''

# Constants
NUM_COLUMNS = 7
NUM_ROWS = 6
type Board = list[list[str]]

# Return a 6x7 board with X or O for the two players and _ representing no piece, [0][0] is the top-left coordinate
def newBoard() -> Board:
    board = []
    for row in range(NUM_ROWS):
        board.append([])
        for col in range(NUM_COLUMNS):
            board[row].append('_')
    return board

# Print out the current board
def printBoard(board: Board):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS):
            print(board[row][col], end='')
        print() # newline
    print("0123456")

def copyBoard(board: Board):
    # Uses list slicing to make a deep copy of the board
    return [col[:] for col in board]

# Return a new board with the given move
def makeMove(player: str, column: int, board: Board):
    newBoard = copyBoard(board)
    if column >= NUM_COLUMNS:
        raise ValueError(
            "column must be less than the number of columns"
        )
    if newBoard[0][column] != '_':
        raise ValueError(
            "illegal move: column is full"
        )
    
    # if this column is empty, add this piece to the bottom
    if newBoard[NUM_ROWS - 1][column] == '_':
        newBoard[NUM_ROWS - 1][column] = player
    # otherwise, find where this piece should drop to
    else:
        for row in range(NUM_ROWS):
            if newBoard[row][column] != '_':
                # we have found the first non-empty space
                newBoard[row - 1][column] = player
                break
    return newBoard

# Return true if the given player has won
def hasWon(player: str, board: Board) -> bool:
    # Check each horizontal for a four-in-a-row
    for row in board:
        for columnNum in range (NUM_COLUMNS - 3):
            if (row[columnNum] == player and
                row[columnNum + 1] == player and
                row[columnNum + 2] == player and
                row[columnNum + 3] == player):
                return True
    
    # Check each vertical
    for columnNum in range(NUM_COLUMNS):
        for rowNum in range(NUM_ROWS - 3):
            if (board[rowNum][columnNum] == player and
                board[rowNum + 1][columnNum] == player and
                board[rowNum + 2][columnNum] == player and
                board[rowNum + 3][columnNum] == player):
                return True
            
    # Check each positive-slope diagonal starting at each column, starting with "3" and ending with the last row
    for columnNum in range(NUM_COLUMNS - 4):
        for startingRowNum in range(3, NUM_ROWS):
            if (board[startingRowNum][columnNum] == player and
                board[startingRowNum - 1][columnNum + 1] == player and
                board[startingRowNum - 2][columnNum + 2] == player and
                board[startingRowNum - 3][columnNum + 3] == player):
                return True
            
    # Check each negative-slope diagonal starting at each column, starting with "0" and ending with the nth - 4 row
    for columnNum in range(NUM_COLUMNS - 4):
        for startingRowNum in range(0, NUM_ROWS - 4):
            if (board[startingRowNum][columnNum] == player and
                board[startingRowNum + 1][columnNum + 1] == player and
                board[startingRowNum + 2][columnNum + 2] == player and
                board[startingRowNum + 3][columnNum + 3] == player):
                return True
            
    # If no win is found...
    return False

def isADraw(board: Board) -> bool:
    for columnNum in range(NUM_COLUMNS):
        if board[0][columnNum] == '_':
            return False
    if hasWon('X', board) or hasWon('O', board):
        return False
    return True
