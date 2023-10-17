import monteCarloSearchTree as mcst
import connectFour as game
from connectFour import Board

PLAYER_SYM = "X"
COMPUTER_SYM = "O"

def getPlayerMove():
    print("Select a column to drop in, 0-" + str(game.NUM_COLUMNS))
    playerInputValid = False
    while (not playerInputValid):
        playerInput = input()
        if playerInput.isdigit() and int(playerInput) >= 0 and int(playerInput) < game.NUM_COLUMNS:
            playerInputValid = True
        else:
            print("Invalid input. Expected number between 0 and " + str(game.NUM_COLUMNS))

def getComputerMove(rootBoard: Board):
    return mcst.monteCarloTreeSearch(rootBoard).columnDroppedIn

def main():
    print("Welcome to Four in a Row! You will make the first move as '" + PLAYER_SYM + "'")
    winner = None
    currentBoard = game.newBoard()
    while(True):
        game.printBoard(currentBoard)

        playerMove = getPlayerMove()
        currentBoard = game.makeMove(PLAYER_SYM, playerMove, currentBoard)
        if game.hasWon(PLAYER_SYM, currentBoard):
            winner = PLAYER_SYM
            break

        computerMove = getComputerMove()
        currentBoard = game.makeMove(COMPUTER_SYM, computerMove, currentBoard)
        if game.hasWon(COMPUTER_SYM, currentBoard):
            winner = COMPUTER_SYM
            break
        

if __name__ == '__main__':
    main()