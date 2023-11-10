"""
Simple Monte Carlo Search Tree
"""
import time
from typing import Self
from connect_four import Board
import connect_four as game
import numpy as np

MAX_SEARCH_TIME = 1000
UCB_CONSTANT = 1.41

INF = float("inf")


class Node:
    def __init__(self, move, parent: Self | None):
        self.move = move
        self.parent = parent
        self.visits = 0
        self.wins = 0
        self.children = {}
        self.winner = game.PLAYERS["none"]

    def add_children(self, children: dict) -> None:
        for child in children:
            self.children[child.move] = child


def get_ucb(node: Node):
    if node.visits == 0:
        return INF
    else:
        return node.wins / node.visits + UCB_CONSTANT * np.sqrt(
            np.log(node.parent.visits) / node.visits
        )


class MonteCarloSearchTree:
    def __init__(self, state=game.ConnectFourState()):
        self.root_state = game.copy_state(state)
        self.root = Node(None, None)

    def select_node(self) -> tuple[Node, game.ConnectFourState]:
        node = self.root
        state = game.copy_state(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_value = get_ucb(max(children, key=get_ucb))
            max_nodes = [node for node in children if get_ucb(node) == max_value]

            node: Node = np.random.choice(max_nodes)
            state = game.make_move(node.move, state)

            if node.visits == 0:
                return node, state

        if expand(node, state):
            node = np.random.choice(list(node.children.values()))
            state = game.make_move(node.move, state)

        return node, state

    def search(self, num_iterations=MAX_SEARCH_TIME):
        for iteration in range(num_iterations):
            node, state = self.select_node()
            outcome = rollout(state)
            backpropogate(node, state.to_play, outcome)

    def best_move(self):
        if game.is_over(self.root_state):
            return -1

        max_value = max(
            self.root.children.values(), key=lambda node: node.visits
        ).visits
        max_nodes = [
            node for node in self.root.children.values() if node.visits == max_value
        ]
        best_child = np.random.choice(max_nodes)

        return best_child.move

    def move(self, move):
        if move in self.root.children:
            self.root_state = game.make_move(move, self.root_state)
            self.root = self.root.children[move]
            return

        self.root_state = game.make_move(move, self.root_state)
        self.root = Node(None, None)


def expand(parent: Node, state: game.ConnectFourState) -> bool:
    if (
        game.has_won(game.PLAYERS["one"], state.board)
        or game.has_won(game.PLAYERS["two"], state.board)
        or game.is_a_draw(state.board)
    ):
        return False

    children = [Node(move, parent) for move in game.get_legal_moves(state)]
    parent.add_children(children)

    return True


def rollout(state: game.ConnectFourState) -> int:
    while not game.is_over(state):
        random_move = np.random.choice(game.get_legal_moves(state))
        state = game.make_move(random_move, state)

    return game.get_winner(state)


def backpropogate(node: Node, whose_turn: int, outcome: int) -> None:
    while node is not None:
        node.visits += 1
        if outcome == whose_turn:
            node.wins += 1
        node = node.parent
        whose_turn = 1 - whose_turn
