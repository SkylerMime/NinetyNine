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

class Stats:
    def __init__(self):
        self.visits = 1 # Always start with 1 visit (this one)
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.meanValue = 0
        self.ucb = 0

    def updateMeanValue(self):
        self.meanValue = (self.wins - self.losses) / (self.wins + self.draws + self.losses)

    def updateUcb(self, parentVisits: int):
        self.ucb = self.meanValue + UCB_CONSTANT * math.sqrt(math.log(parentVisits) / self.visits)

# MCST Node
class Node:
    def __init__(self, parent: Self, children: list[Self], stats: Stats):
        self.parent = parent
        self.children = children
        self.stats = stats

    def updateStats(self, newResult):
        if newResult == 1:
            self.stats.wins += 1
        elif newResult == 0:
            self.stats.draws += 1
        elif newResult == -1:
            self.stats.losses += 1
        else:
            raise ValueError("unexpected value in result")
        self.stats.updateMeanValue()

        self.stats.updateUcb(self.parent.stats.visits)
    
    def isRoot(self):
        return self.parent == None
    
# Specific node for Connect4 (Inheritance)
class ConnectFour(Node):
    def __init__(self, parent: Self, children: list[Self], stats: Stats, boardState: Board, columnDroppedIn: int, activePlayer: str):
        super().__init__(parent, children, stats)
        self.boardState = boardState
        self.activePlayer = activePlayer
        self.isFullyExpanded = False
        # since each turn involves the player dropping a disc into a column, this node stores the column dropped into for this turn

    '''
    Do expansion by randomly picking a move that hasn't been explored yet from this state

    Raises IndexError if all moves from this state have been explored
    '''
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

        # Create and return this child node
        newChild = ConnectFour(
            self,
            [],
            None,
            game.makeMove(nextPlayer, moveToMake, self.boardState),
            moveToMake,
            nextPlayer
        )
        self.children.append(newChild)
        return newChild
    
    '''
    Check to see if this move brought the game into a win condition

    Returns true if this move resulted in a win for the active player
    '''
    def isTerminal(self):
        return game.hasWon(self.activePlayer, self.boardState)

'''
Get the result of this rollout

Returns +1 for a win for the computer, 0 for a draw, and -1 for a loss for the computer.
'''
def result(node: ConnectFour) -> int:
    if node.isTerminal():
        if node.activePlayer == COMPUTER_PLAYER:
            return 1
        elif node.activePlayer == OPPOSING_PLAYER:
            return -1

# main function
def monteCarloTreeSearch(root: ConnectFour):

    for iteration in range(MAX_SEARCH_TIME):
        leaf = traverse(root)
        simulationResult = rollout(leaf)
        backpropogate(leaf, simulationResult)

    return bestChild(root)

# ranking function helper
def getUcb(node):
    return node.stats.ucb

# ranking function
def bestUcb(children: list[ConnectFour]):
    children.sort(key=getUcb)
    return children[0]

# node traversal function
def traverse(node: ConnectFour):
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
    return result(node)

# get a random child node
def rolloutPolicy(node):
    return random.choice(node.children)

# backpropogation function
def backpropogate(node: ConnectFour, result):
    if node.isRoot():
        return
    node.updateStats(result)
    backpropogate(node.parent)

def getNumVisits(node: ConnectFour):
    return node.stats.visits

# select the best child node with the highest number of visits
def bestChild(node: ConnectFour) -> ConnectFour:
    node.children.sort(key=getNumVisits)
    return node.children[0]

