import math
import random
from experiments import monte_carlo_search_tree as mcst
from experiments import connect_four as game


class TestNode:
    def setup_method(self):
        self.root = mcst.Node(None)
        self.child = mcst.Node(self.root)
        self.winning_child = mcst.Node(self.root)
        self.losing_child = mcst.Node(self.root)
        self.root.children.append(self.winning_child)

        self.root.visits = 4

        self.winning_child.visits = 12
        self.winning_child.wins = 7
        self.winning_child.losses = 3
        self.winning_child.draws = 2

        self.losing_child.visits = 17
        self.losing_child.wins = 6
        self.losing_child.losses = 7
        self.losing_child.draws = 4

    def test_update_stats(self):
        self.child.update_stats(1)
        assert self.child.wins == 1
        assert self.child.losses == 0
        assert self.child.draws == 0

    def test_is_root(self):
        assert self.root.is_root()
        assert not self.child.is_root()

    def test_mean_value(self):
        assert self.winning_child.get_mean_value() == 1 / 3
        assert self.losing_child.get_mean_value() == -1 / 17

    def test_ucb(self):
        assert self.winning_child.get_ucb() == 1 / 3 + mcst.UCB_CONSTANT * math.sqrt(
            math.log(4) / 12
        )
        assert self.losing_child.get_ucb() == -1 / 17 + mcst.UCB_CONSTANT * math.sqrt(
            math.log(4) / 17
        )


class TestConnectFour:
    def setup_method(self):
        self.root_board = game.new_board()
        self.root_board = game.make_move("O", 3, self.root_board)
        self.root = mcst.ConnectFourNode(None, self.root_board, 3, "O")

        random.seed(300)
        self.initial_state = random.getstate()
        random.setstate(self.initial_state)

    def test_create_unexplored_child_of_root(self):
        col_to_drop_in = random.choice([0, 1, 2, 4, 5, 6])
        new_child_comparison_board = game.make_move(
            "X", col_to_drop_in, self.root_board
        )
        new_child_comparison = mcst.ConnectFourNode(
            self.root, new_child_comparison_board, col_to_drop_in, "X"
        )
        random.setstate(self.initial_state)
        new_child = self.root.create_unexplored_child()

        assert new_child.board_state == new_child_comparison.board_state

    def test_manually_add_children(self):
        self.child_board = self.root_board.copy()
        self.child_board = game.make_move("X", 3, self.child_board)
        self.child = mcst.ConnectFourNode(self.root, self.child_board, 3, "X")
        self.root.children.append(self.child)

        self.root.create_unexplored_child()

        assert len(self.root.children) == 2

    def test_create_all_the_children_throws_error(self):
        for i in range(game.NUM_COLUMNS):
            self.root.create_unexplored_child()
        with pytest.raises(IndexError):
            self.root.create_unexplored_child()

    def test_filling_a_column_unexplored_children_will_yield(self):
        full_test_board = [
            ["_", "O", "_", "_", "_", "O", "X"],
            ["_", "X", "_", "_", "_", "X", "O"],
            ["O", "O", "_", "_", "X", "X", "O"],
            ["X", "X", "X", "O", "O", "O", "X"],
            ["O", "O", "X", "X", "O", "X", "O"],
            ["X", "X", "O", "X", "O", "O", "X"],
        ]
        self.root = mcst.ConnectFourNode(None, full_test_board, 0, "O")
        self.root.create_unexplored_child()
