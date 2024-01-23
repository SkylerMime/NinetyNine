import random
import time
import math
from copy import deepcopy

from connect_four.connect_four_state import ConnectState
from connect_four.constants import GameConstants, MCTSConstants


class Node:
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.visits = 0
        self.wins = 0
        self.children = {}
        self.outcome = GameConstants.PLAYERS["none"]

    def add_children(self, children: dict | list) -> None:
        for child in children:
            self.children[child.move] = child

    def value(self, explore: float = MCTSConstants.EXPLORATION):
        if self.visits == 0:
            return 0 if explore == 0 else GameConstants.INF
        else:
            return self.wins / self.visits + explore * math.sqrt(
                math.log(self.parent.visits) / self.visits
            )


def roll_out(state: ConnectState) -> int:
    while not state.game_over():
        state.move(random.choice(state.get_legal_moves()))

    return state.get_outcome()


def back_propagate(node: Node, turn: int, outcome: int) -> None:
    # For the current player, not the next player
    reward = 0 if outcome == turn else 1

    while node is not None:
        node.visits += 1
        node.wins += reward
        node = node.parent
        if outcome == GameConstants.OUTCOMES["draw"]:
            reward = 0
        else:
            reward = 1 - reward


def expand(parent: Node, state: ConnectState) -> bool:
    if state.game_over():
        return False

    children = [Node(move, parent) for move in state.get_legal_moves()]
    parent.add_children(children)

    return True


class MCTS:
    def __init__(self, state=ConnectState()):
        self.root_state = deepcopy(state)
        self.root = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0

    def select_node(self) -> tuple[Node, ConnectState]:
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]

            node = random.choice(max_nodes)
            state.move(node.move)

            if node.visits == 0:
                return node, state

        if expand(node, state):
            node = random.choice(list(node.children.values()))
            state.move(node.move)

        return node, state

    def search(self, time_limit: int):
        start_time = time.process_time()

        num_rollouts = 0
        while time.process_time() - start_time < time_limit:
            node, state = self.select_node()
            outcome = roll_out(state)
            back_propagate(node, state.to_play, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    def best_move(self):
        if self.root_state.game_over():
            return -1

        max_value = max(self.root.children.values(), key=lambda n: n.visits).visits
        max_nodes = [n for n in self.root.children.values() if n.visits == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move

    def move(self, move):
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
            return

        self.root_state.move(move)
        self.root = Node(None, None)

    def statistics(self) -> tuple:
        return self.num_rollouts, self.run_time
