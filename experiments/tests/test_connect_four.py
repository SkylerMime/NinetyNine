from experiments import connect_four as game


class TestBoardSetup:
    def setup_method(self):
        self.board_0 = game.create_board()
        self.board_1 = game.create_board()
        self.board_1[game.NUM_ROWS - 1][game.NUM_COLUMNS - 1] = "X"
        self.board_2 = game.create_board()
        self.board_2[game.NUM_ROWS - 1][game.NUM_COLUMNS - 1] = "X"
        self.board_2[game.NUM_ROWS - 2][game.NUM_COLUMNS - 1] = "O"
        self.full_col_board = game.create_board()
        for row in range(game.NUM_ROWS):
            self.full_col_board[row][2] = "X"
        self.win_o_board = game.create_board()
        self.win_o_board[game.NUM_ROWS - 1][3] = "X"
        for row in range(game.NUM_ROWS - 5, game.NUM_ROWS - 1):
            self.win_o_board[row][3] = "O"
        self.win_x_board = game.create_board()
        self.comparison_board = game.create_board()
        self.comparison_board[game.NUM_ROWS - 1][0] = "X"
        self.comparison_board[game.NUM_ROWS - 1][1] = "O"
        self.comparison_board[game.NUM_ROWS - 2][1] = "X"
        self.col_two_comparison_board = game.create_board()
        self.col_two_comparison_board[game.NUM_ROWS - 1][2] = "X"
        self.col_two_comparison_board[game.NUM_ROWS - 2][2] = "O"
        self.col_two_comparison_board[game.NUM_ROWS - 3][2] = "X"

    def test_make_move(self):
        self.board_0 = game.make_move("X", game.NUM_COLUMNS - 1, self.board_0)
        assert self.board_0 == self.board_1

        self.board_1 = game.make_move("O", game.NUM_COLUMNS - 1, self.board_1)
        assert self.board_1 == self.board_2

        self.win_x_board = game.make_move("X", 0, self.win_x_board)
        self.win_x_board = game.make_move("O", 1, self.win_x_board)
        self.win_x_board = game.make_move("X", 1, self.win_x_board)
        assert self.win_x_board == self.comparison_board

        with pytest.raises(ValueError):
            game.make_move("O", game.NUM_COLUMNS, self.board_1)
        with pytest.raises(ValueError):
            game.make_move("O", 2, self.full_col_board)

    def test_make_move_has_no_side_effects(self):
        create_board = game.make_move("X", 0, self.board_0)
        assert self.board_0 != create_board

    def test_make_move_leaves_column_unchanged(self):
        create_board = game.make_move("X", 2, self.board_0)
        create_board = game.make_move("O", 2, create_board)
        create_board = game.make_move("X", 2, create_board)
        assert create_board == self.col_two_comparison_board

    def test_has_won_finds_diagonal_win(self):
        assert game.has_won("O", self.win_o_board)
        assert not game.has_won("X", self.win_o_board)

        # board with diagonal 'X' win
        self.win_x_board = game.create_board()
        moves = [0, 1, 1, 2, 2, 2, 3, 3, 3, 3]
        for move in moves:
            self.win_x_board = game.make_move(
                "X" if len(moves) % 2 == 0 else "O", move, self.win_x_board
            )
        assert game.has_won("X", self.win_x_board)
        assert not game.has_won("O", self.win_x_board)

    def test_has_won_finds_vertical_win(self):
        self.win_x_board = game.create_board()
        for _ in range(4):
            self.win_x_board = game.make_move("X", 2, self.win_x_board)
        assert game.has_won("X", self.win_x_board)
        assert not game.has_won("O", self.win_x_board)

    def test_has_won_finds_horizontal_win(self):
        win_o_board = [
            ["X", "X", "O", "O", "X", "O", "X"],
            ["O", "X", "X", "O", "X", "X", "X"],
            ["O", "O", "O", "X", "X", "O", "O"],
            ["X", "X", "X", "O", "O", "O", "O"],
            ["O", "O", "X", "X", "X", "O", "X"],
            ["X", "O", "X", "O", "O", "X", "O"],
        ]
        assert game.has_won("O", win_o_board)
        assert not game.has_won("X", win_o_board)

    def test_is_a_draw_finds_a_draw(self):
        draw_board = [
            ["X", "X", "O", "O", "X", "O", "X"],
            ["O", "X", "X", "O", "X", "X", "X"],
            ["O", "O", "O", "X", "X", "O", "O"],
            ["X", "X", "X", "O", "O", "O", "X"],
            ["O", "O", "X", "X", "X", "O", "X"],
            ["X", "O", "X", "O", "O", "X", "O"],
        ]
        assert game.is_a_draw(draw_board)
