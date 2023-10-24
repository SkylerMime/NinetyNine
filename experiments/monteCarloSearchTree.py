'''
Simple Monte Carlo Search Tree
Implementation based on GeeksForGeeks: https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
This page was helpful as well: https://towardsdatascience.com/monte-carlo-tree-search-an-introduction-503d8c04e168
'''

from typing import Self
import random, math
from connectFour import Board
import connectFour as game

MAX_SEARCH_TIME = 1000
COMPUTER_PLAYER = 'X'
OPPOSING_PLAYER = 'O'
UCB_CONSTANT = 1.41 # TODO: I don't actually know what the best value for this constant is

# MCST Node
class Node:
    def __init__(self, parent: Self):
        self.parent = parent
        self.children: list[Self] = []
        self.visits = 0
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
        if self.wins == 0 and self.draws == 0 and self.losses == 0:
            return 0
        return (self.wins - self.losses) / (self.wins + self.draws + self.losses)

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
    def __init__(self, parent: Self, boardState: Board, columnDroppedIn: int, activePlayer: str):
        super().__init__(parent)
        self.boardState = boardState.copy() # we store a copy of the board to prevent side effects
        self.columnDroppedIn = columnDroppedIn
        self.activePlayer = activePlayer
        self.isFullyExpanded = False

    def createUnexploredChild(self):
        # Find all the moves that haven't been made yet by the children, that don't result in a full column
        unexploredColumns = list(range(game.NUM_COLUMNS))
        for child in self.children:
            if child.columnDroppedIn in unexploredColumns.copy():
                unexploredColumns.remove(child.columnDroppedIn)
        if len(unexploredColumns) == 0:
            self.isFullyExpanded = True
            raise IndexError("All moves from this state have been explored")
        for column in unexploredColumns.copy(): # copy is needed for the iteration to work properly
            if self.boardState[0][column] != '_':
                unexploredColumns.remove(column)

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
        if game.hasWon(self.activePlayer, self.boardState):
            return True
        if game.isADraw(self.boardState):
            return True
        return False

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
    if len(node.children) < 1:
        node.createUnexploredChild()
    return random.choice(node.children)

# backpropogation function
def backpropogate(node: ConnectFourNode, result):
    node.updateStats(result)
    node.visits += 1
    if node.isRoot():
        return
    backpropogate(node.parent, result)

def getNumVisits(node: ConnectFourNode):
    return node.visits

# select the best child node with the highest number of visits
def bestChild(node: ConnectFourNode) -> ConnectFourNode:
    node.children.sort(key=getNumVisits)
    return node.children[0]

