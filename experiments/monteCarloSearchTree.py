'''
Simple Monte Carlo Search Tree
Implementation based on GeeksForGeeks: https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
This page was helpful as well: https://towardsdatascience.com/monte-carlo-tree-search-an-introduction-503d8c04e168
And I used this to test to see what I was doing wrong: https://ai-boson.github.io/mcts/
'''

from typing import Self
import random, math
from connectFour import Board
import connectFour as game
import numpy as np

MAX_SEARCH_TIME = 10000
COMPUTER_PLAYER = 'X'
OPPOSING_PLAYER = 'O'
TIE_GAME = "DRAW"
UCB_CONSTANT = 1.41

# MCST Node
class Node:
    def __init__(self, parent: Self):
        self.parent = parent
        self.children: list[Self] = []
        self.visits = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        
    def getMeanValue(self):
        if self.wins == 0 and self.draws == 0 and self.losses == 0:
            return 0
        return (self.wins - self.losses) / (self.visits)

    def getUcb(self):
        if self.parent == None:
            raise ValueError("ucb called on the root")
        if self.visits == 0:
            return math.inf
        if self.parent.visits == 0:
            raise ValueError("no parent visits")
        return self.getMeanValue() + UCB_CONSTANT * math.sqrt(math.log(self.parent.visits) / self.visits)
    
# Specific node for Connect4 (Inheritance)
class ConnectFourNode(Node):
    def __init__(self, parent: Self, boardState: Board, parentColumnDroppedIn: int, activePlayer: str):
        super().__init__(parent)
        self.boardState = boardState.copy() # we store a copy of the board to prevent side effects
        self.parentColumnDroppedIn = parentColumnDroppedIn
        self.activePlayer = activePlayer
        self.isFullyExpanded = False
        self.untriedActions = getLegalColumns(boardState)
    
    def isTerminal(self):
        return isGameOver(self.boardState)
    
def getWinner(boardState: Board):
    if game.hasWon(OPPOSING_PLAYER, boardState):
        return OPPOSING_PLAYER
    elif game.hasWon(COMPUTER_PLAYER, boardState):
        return COMPUTER_PLAYER
    elif game.isADraw(boardState):
        return TIE_GAME
    else:
        return None
    
def isGameOver(boardState: Board):
    return getWinner(boardState) != None
    
def getLegalColumns(board: Board):
    legalColumns = list(range(game.NUM_COLUMNS))
    for column in legalColumns.copy():
        if board[0][column] != '_':
            legalColumns.remove(column)
    return legalColumns

def expand(node: ConnectFourNode):
    columnToDropIn = node.untriedActions.pop()
    if len(node.untriedActions) == 0:
        node.isFullyExpanded = True
    nextPlayer = getNextPlayer(node.activePlayer)
    nextBoard = game.makeMove(nextPlayer, columnToDropIn, node.boardState)
    childNode = ConnectFourNode(node, nextBoard, columnToDropIn, nextPlayer)

    node.children.append(childNode)
    return childNode

def getNextPlayer(player: str) -> str:
    if player == COMPUTER_PLAYER:
        return OPPOSING_PLAYER
    else:
        return COMPUTER_PLAYER

# Returns +1 for a win for the computer and -1 for a loss for the computer.
def getRolloutResult(finalBoard: Board) -> int:
    winner = getWinner(finalBoard)
    if winner == None:
        raise ValueError("board is not in a game over state")
    else:
        if winner == TIE_GAME:
            return 0
        elif winner == COMPUTER_PLAYER:
            return 1
        elif winner == OPPOSING_PLAYER:
            return -1

# main function
def monteCarloTreeSearch(root: ConnectFourNode):

    for iteration in range(MAX_SEARCH_TIME):
        leaf = traverse(root)
        simulationResult = rollout(leaf.boardState, root.activePlayer)
        backpropogate(leaf, simulationResult)

    return bestChild(root)

# ranking function helper
def getUcb(node: ConnectFourNode):
    return node.getUcb()

# ranking function
def bestUcb(children: list[ConnectFourNode]):
    children.sort(key=getUcb)
    return children[0]

def traverse(node: ConnectFourNode):
    while not node.isTerminal():
        if not node.isFullyExpanded:
            return expand(node)
        else:
            node = bestChild(node)
    return node

# rollout the game state from this state until there is an outcome.
# importantly, this does not cause tree creation.
# moves are selected randomly (light playout)
def rollout(boardState: Board, player: str):
    while not isGameOver(boardState):
        nextPlayer = getNextPlayer(player)
        possibleMoves = getLegalColumns(boardState)
        columnToDropIn = random.choice(possibleMoves)
        boardState = game.makeMove(nextPlayer, columnToDropIn, boardState)
    return getRolloutResult(boardState)

# backpropogation function
def backpropogate(node: ConnectFourNode, result):
    node.visits += 1
    if result == 1:
        node.wins += 1
    elif result == -1:
        node.losses += 1
    elif result == 0:
        node.draws += 1
    
    if not node.parent:
        return
    backpropogate(node.parent, result)

def getNumVisits(node: ConnectFourNode):
    return node.visits

# select the best child node with the highest number of visits
def bestChild(node: ConnectFourNode) -> ConnectFourNode:
    node.children.sort(key=getNumVisits)
    return node.children[0]

