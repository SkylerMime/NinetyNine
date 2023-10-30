import monteCarloSearchTree as mcst
import connectFour as game
from connectFour import Board

PLAYER_SYM = "X"
COMPUTER_SYM = "O"

def getPlayerMove():
    print("Select a column to drop in, 0-" + str(game.NUM_COLUMNS - 1))
    playerInputValid = False
    while (not playerInputValid):
        playerInput = input()
        if playerInput.isdigit() and int(playerInput) >= 0 and int(playerInput) < game.NUM_COLUMNS:
            playerInputValid = True
        else:
            print("Invalid input. Expected number between 0 and " + str(game.NUM_COLUMNS - 1))
    return int(playerInput)

def getComputerMove(rootState: mcst.ConnectFourNode):
    return mcst.monteCarloTreeSearch(rootState).parentColumnDroppedIn

def main():
    print("Welcome to Four in a Row! You will make the first move as '" + PLAYER_SYM + "'")
    winner = None
    currentBoard = game.newBoard()
    game.printBoard(currentBoard)
    while(True):
        playerMove = getPlayerMove()
        currentBoard = game.makeMove(PLAYER_SYM, playerMove, currentBoard)
        game.printBoard(currentBoard)
        currentGameState = mcst.ConnectFourNode(None, currentBoard, playerMove, PLAYER_SYM)
        if game.hasWon(PLAYER_SYM, currentBoard):
            winner = PLAYER_SYM
            break

        computerMove = getComputerMove(currentGameState)
        currentBoard = game.makeMove(COMPUTER_SYM, computerMove, currentBoard)
        game.printBoard(currentBoard)
        if game.hasWon(COMPUTER_SYM, currentBoard):
            winner = COMPUTER_SYM
            break

    print("The " + winner + " has won! Play again?")
        

if __name__ == '__main__':
    main()