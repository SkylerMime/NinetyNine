'''
Simple Monte Carlo Search Tree
Implementation based on GeeksForGeeks: https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
This page was helpful as well: https://towardsdatascience.com/monte-carlo-tree-search-an-introduction-503d8c04e168
'''

from typing import Self
import random, math
from connectFour import Board
import connectFour as game

MAX_SEARCH_TIME = 1000000
COMPUTER_PLAYER = 'X'
OPPOSING_PLAYER = 'O'
UCB_CONSTANT = 0.3 # TODO: I don't actually know what the best value for this constant is

# MCST Node
class Node:
    def __init__(self, parent: Self):
        self.parent = parent
        self.children: list[Self] = []
        self.visits = 1 # Always start with 1 visit (this one)
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def isRoot(self):
        return self.parent == None

    def updateStats(self, newResult):
        if newResult == 1:
            self.wins += 1
        elif newResult == 0:
            self.draws += 1
        elif newResult == -1:
            self.losses += 1
        else:
            raise ValueError("unexpected value in result")
        
    def getMeanValue(self):
        return (self.wins - self.losses) / (self.wins + self.draws + self.losses)

    def getUcb(self):
        return self.getMeanValue() + UCB_CONSTANT * math.sqrt(math.log(self.parent.visits) / self.visits)
    
# Specific node for Connect4 (Inheritance)
class ConnectFourNode(Node):
    def __init__(self, parent: Self, boardState: Board, columnDroppedIn: int, activePlayer: str):
        super().__init__(parent)
        self.boardState = boardState.copy() # we store a copy of the board to prevent side effects
        self.columnDroppedIn = columnDroppedIn
        self.activePlayer = activePlayer
        self.isFullyExpanded = False

    def createUnexploredChild(self):
        # Find all the moves that haven't been made yet by the children
        unexploredColumns = list(range(game.NUM_COLUMNS))
        for child in self.children:
            if child.columnDroppedIn in unexploredColumns:
                unexploredColumns.remove(child.columnDroppedIn)
        if len(unexploredColumns) == 0:
            self.isFullyExpanded = True
            raise IndexError("All moves from this state have been explored")

        # Choose a random column to drop the disc into
        moveToMake = random.choice(unexploredColumns)

        if self.activePlayer == 'X':
            nextPlayer = 'O'
        else:
            nextPlayer = 'X'

        newChild = ConnectFourNode(
            self,
            game.makeMove(nextPlayer, moveToMake, self.boardState),
            moveToMake,
            nextPlayer
        )
        self.children.append(newChild)
        return newChild
    
    def isTerminal(self):
        return game.hasWon(self.activePlayer, self.boardState)

# Returns +1 for a win for the computer and -1 for a loss for the computer.
def getRolloutResult(node: ConnectFourNode) -> int:
    # TODO: Implement draw
    if node.isTerminal():
        if node.activePlayer == COMPUTER_PLAYER:
            return 1
        elif node.activePlayer == OPPOSING_PLAYER:
            return -1
    else:
        raise ValueError("node must be terminal")

# main function
def monteCarloTreeSearch(root: ConnectFourNode):

    for iteration in range(MAX_SEARCH_TIME):
        leaf = traverse(root)
        simulationResult = rollout(leaf)
        backpropogate(leaf, simulationResult)

    return bestChild(root)

# ranking function helper
def getUcb(node: ConnectFourNode):
    return node.getUcb()

# ranking function
def bestUcb(children: list[ConnectFourNode]):
    children.sort(key=getUcb)
    return children[0]

# node traversal function
def traverse(node: ConnectFourNode):
    while node.isFullyExpanded:
        node = bestUcb(node.children)

    # see if this is a leaf node
    try:
        return node.createUnexploredChild()
    except IndexError:
        return node

# function for the result of the simulation
def rollout(node):
    while not node.isTerminal():
        node = rolloutPolicy(node)
    return getRolloutResult(node)

# get a random child node
def rolloutPolicy(node):
    return random.choice(node.children)

# backpropogation function
def backpropogate(node: ConnectFourNode, result):
    if node.isRoot():
        return
    node.updateStats(result)
    backpropogate(node.parent)

def getNumVisits(node: ConnectFourNode):
    return node.stats.visits

# select the best child node with the highest number of visits
def bestChild(node: ConnectFourNode) -> ConnectFourNode:
    node.children.sort(key=getNumVisits)
    return node.children[0]

