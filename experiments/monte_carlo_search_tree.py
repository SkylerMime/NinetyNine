"""
Simple Monte Carlo Search Tree
Implementation based on GeeksForGeeks: https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
This page was helpful as well: https://towardsdatascience.com/monte-carlo-tree-search-an-introduction-503d8c04e168
And I used this to test to see what I was doing wrong: https://ai-boson.github.io/mcts/
"""

from typing import Self
import math
from connect_four import Board
import connect_four as game
import numpy as np

MAX_SEARCH_TIME = 1000
COMPUTER_PLAYER = "X"
OPPOSING_PLAYER = "O"
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

    def get_mean_value(self):
        if self.wins == 0 and self.draws == 0 and self.losses == 0:
            return 0
        return (self.wins - self.losses) / self.visits

    def get_ucb(self):
        if self.parent is None:
            raise ValueError("ucb called on the root")
        if self.visits == 0:
            return math.inf
        if self.parent.visits == 0:
            raise ValueError("no parent visits")
        return self.get_mean_value() + UCB_CONSTANT * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )


# Specific node for Connect4 (Inheritance)
class ConnectFourNode(Node):
    def __init__(
        self,
        parent: Self | None,
        board_state: Board,
        parent_column_dropped_in: int,
        active_player: str,
    ):
        super().__init__(parent)
        self.boardState = (
            board_state.copy()
        )  # we store a copy of the board to prevent side effects
        self.parentColumnDroppedIn = parent_column_dropped_in
        self.activePlayer = active_player
        self.isFullyExpanded = False
        self.untriedActions = get_legal_columns(board_state)

    def is_terminal(self):
        return is_game_over(self.boardState)


def get_winner(board_state: Board):
    if game.has_won(OPPOSING_PLAYER, board_state):
        return OPPOSING_PLAYER
    elif game.has_won(COMPUTER_PLAYER, board_state):
        return COMPUTER_PLAYER
    elif game.is_a_draw(board_state):
        return TIE_GAME
    else:
        return None


def is_game_over(board_state: Board):
    return get_winner(board_state) is not None


def get_legal_columns(board: Board):
    legal_columns = list(range(game.NUM_COLUMNS))
    for column in legal_columns.copy():
        if board[0][column] != "_":
            legal_columns.remove(column)
    return legal_columns


def expand(node: ConnectFourNode):
    column_to_drop_in = node.untriedActions.pop()
    if len(node.untriedActions) == 0:
        node.isFullyExpanded = True
    next_player = get_next_player(node.activePlayer)
    next_board = game.make_move(next_player, column_to_drop_in, node.boardState)
    child_node = ConnectFourNode(node, next_board, column_to_drop_in, next_player)

    node.children.append(child_node)
    return child_node


def get_next_player(player: str) -> str:
    if player == COMPUTER_PLAYER:
        return OPPOSING_PLAYER
    else:
        return COMPUTER_PLAYER


# Returns +1 for a win for the computer and -1 for a loss for the computer.
def get_rollout_result(final_board: Board) -> int:
    winner = get_winner(final_board)
    if winner is None:
        raise ValueError("board is not in a game over state")
    else:
        if winner == TIE_GAME:
            return 0
        elif winner == COMPUTER_PLAYER:
            return 1
        elif winner == OPPOSING_PLAYER:
            return -1


# main function
def monte_carlo_tree_search(root: ConnectFourNode):
    for iteration in range(MAX_SEARCH_TIME):
        leaf = traverse(root)
        simulation_result = rollout(leaf.boardState, root.activePlayer)
        backpropogate(leaf, simulation_result)

    return best_child(root)


# ranking function helper
def get_ucb(node: ConnectFourNode):
    return node.get_ucb()


# ranking function
def best_ucb(children: list[ConnectFourNode]):
    children.sort(key=get_ucb)
    return children[0]


def traverse(node: ConnectFourNode):
    while not node.is_terminal():
        if not node.isFullyExpanded:
            return expand(node)
        else:
            node = best_ucb(node.children)
    return node


# rollout the game state from this state until there is an outcome.
# importantly, this does not cause tree creation.
# moves are selected randomly (light playout)
def rollout(board_state: Board, player: str):
    next_player = player
    while not is_game_over(board_state):
        next_player = get_next_player(next_player)
        possible_moves = get_legal_columns(board_state)
        column_to_drop_in = np.random.choice(possible_moves)
        board_state = game.make_move(next_player, column_to_drop_in, board_state)
    return get_rollout_result(board_state)


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


def get_num_visits(node: ConnectFourNode):
    return node.visits


# select the best child node with the highest number of visits
# possible problem: This should choose randomly from all nodes with "4" values, e.g.
def best_child(node: ConnectFourNode) -> ConnectFourNode:
    node.children.sort(key=get_num_visits)
    return node.children[0]
