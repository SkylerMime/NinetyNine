"""
Monte Carlo Tree Search algorithm for NinetyNine
The algorithm as currently implemented makes
decisions according to the actual game state, rather
than the limited information a player would have access to.
This means that the AI will know all the cards in the other player's hands.
"""

from __future__ import annotations

import random
import time

from ninety_nine.ninety_nine_state import GameState, Card, Scores
import ninety_nine.ninety_nine_state as game
import math

type ChildNodes = dict[Card, Node]

AI_PLAYER_NUM = 0
EXPLORATION = math.sqrt(2)
INF = float("inf")


class Node:
    def __init__(self, card_played: Card | None, parent: Node | None):
        self.card_played = card_played
        self.parent = parent
        self.visits = 0
        # we use "made_bids," but other possibilities are:
        #     - "wins"
        #     - "earned_points
        # TODO: Implement these alternate strategies
        self.players_total_made_bids = {player_num: 0 for player_num in range(3)}
        self.children: dict[Card, Node] = {}
        self.players_made_bid = {}

    def add_children(self, children: ChildNodes):
        for child in children:
            self.children[child.card_played] = child

    def value(self, explore: float = EXPLORATION):
        if self.visits == 0:
            return 0 if explore == 0 else INF
        else:
            return self.players_total_made_bids[
                AI_PLAYER_NUM
            ] / self.visits + explore * math.sqrt(
                math.log(self.parent.visits) / self.visits
            )


def roll_out(state: GameState) -> Scores:
    while not game.game_is_over(state):
        current_player = state.next_to_play
        if current_player is None:
            state = game.finish_trick(state)
            current_player = state.next_to_play
        if state.next_to_play is None:
            break  # TODO: Refactor this to avoid repetition
        random_card_play = random.choice(
            list(game.get_legal_card_plays(state, current_player))
        )
        state = game.make_card_play(state, current_player, random_card_play)

    scores = game.get_scores(state)
    return scores


def back_propagate(node: Node, result_scores: Scores):
    players_making_bid = {
        player_num: 1 if result_scores[player_num] > 9 else 0 for player_num in range(3)
    }
    while node is not None:
        node.visits += 1
        node.players_total_made_bids = {
            player_num: node.players_total_made_bids[player_num]
            + players_making_bid[player_num]
            for player_num in range(3)
        }
        node = node.parent


def expand(parent: Node, state: GameState) -> bool:
    if game.is_full(state.current_trick):
        state = game.finish_trick(state)
    if game.game_is_over(state):
        return False

    children = [
        Node(card_played, parent)
        for card_played in game.get_legal_card_plays(state, state.next_to_play)
    ]
    parent.add_children(children)

    return True


class NinetyNineMCST:
    def __init__(self, state=GameState()):
        self.root_state = state.copy_state()
        self.root = Node(None, None)

    def select_node(self):
        node = self.root
        state = self.root_state.copy_state()

        while node.children:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]

            node: Node = random.choice(max_nodes)
            if game.is_full(state.current_trick):
                state = game.finish_trick(state)
            state = game.make_card_play(state, state.next_to_play, node.card_played)

            if node.visits == 0:
                return node, state

        if expand(node, state):
            node = random.choice(list(node.children.values()))
            if game.is_full(state.current_trick):
                state = game.finish_trick(state)
            game.make_card_play(state, state.next_to_play, node.card_played)

        return node, state

    def search(self, time_limit: int):
        start_time = time.process_time()

        num_rollouts = 0
        while time.process_time() - start_time < time_limit:
            node, state = self.select_node()
            final_scores = roll_out(state)
            back_propagate(node, final_scores)
            num_rollouts += 1

    def best_move(self):
        if game.game_is_over(self.root_state):
            raise KeyError("The game has ended")

        max_value = max(self.root.children.values(), key=lambda n: n.visits).visits
        max_nodes = [n for n in self.root.children.values() if n.visits == max_value]
        best_child: Node = random.choice(max_nodes)

        return best_child.card_played

    def play_card(self, card):
        if game.is_full(self.root_state.current_trick):
            self.root_state = game.finish_trick(self.root_state)
        self.root_state = game.make_card_play(
            self.root_state, self.root_state.next_to_play, card
        )
        if card in self.root.children:
            self.root = self.root.children[card]
        else:
            self.root = Node(None, None)
