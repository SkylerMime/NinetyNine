'''
Simple Monte Carlo Search Tree
Implementation based on GeeksForGeeks: https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
'''

from typing import Self
import random

MAX_SEARCH_TIME = 1000000

class Stats:
    def __init__(self, visits: int):
        self.visits = visits

# MCST Node
class Node:
    def __init__(self, parent: Self, children: list[Self], stats: Stats):
        self.parent = parent
        self.children = children
        self.stats = stats

    def isNonTerminal(self):
        return len(self.children) > 0


# main function
def monteCarloTreeSearch(root: Node):

    for iteration in range(MAX_SEARCH_TIME):
        leaf = traverse(root)
        simulationResult = rollout(leaf)
        backpropogate(leaf, simulationResult)

    return bestChild(root)

# node traversal function
def traverse(node):
    while fullyExpanded(node):
        node = bestUct(node)

    # if this is a leaf node
    return pickUnvisited(node.children) or node

# function for the result of the simulation
def rollout(node):
    while node.isNonTerminal():
        node = rolloutPolicy(node)
    return result(node)

# get a random child node
def rolloutPolicy(node):
    return random.choice(node.children)

# backpropogation function
def backpropogate(node, result):
    if isRoot(node):
        return
    node.stats = updateStats(node, result)
    backpropogate(node.parent)

# select the best child node
# with the highest number of visits
def bestChild(node):
    return childWithHighestNumberOfVisits