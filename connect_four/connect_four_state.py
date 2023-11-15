from copy import deepcopy
import numpy as np
from constants import GameConstants


class ConnectState:
    def __init__(self):
        self.board = [[0] * GameConstants.COLS for _ in range(GameConstants.ROWS)]
        self.to_play = GameConstants.PLAYERS["one"]
        self.height = [GameConstants.ROWS - 1] * GameConstants.COLS
        self.last_played = []

    def get_board(self):
        return deepcopy(self.board)

    def move(self, col):
        self.board[self.height[col]][col] = self.to_play
        self.last_played = [self.height[col], col]
        self.height[col] -= 1
        self.to_play = (
            GameConstants.PLAYERS["two"]
            if self.to_play == GameConstants.PLAYERS["one"]
            else GameConstants.PLAYERS["one"]
        )

    def get_legal_moves(self):
        return [col for col in range(GameConstants.COLS) if self.board[0][col] == 0]

    def check_win(self):
        if len(self.last_played) > 0 and self.check_win_from(
            self.last_played[0], self.last_played[1]
        ):
            return self.board[self.last_played[0]][self.last_played[1]]
        return 0

    def check_win_from(self, row, col):
        player = self.board[row][col]
        """
        Last played action is at (row, col)
        Check surrounding 7x7 grid for a win
        """

        consecutive = 1
        # Check horizontal
        tmprow = row
        while tmprow + 1 < GameConstants.ROWS and self.board[tmprow + 1][col] == player:
            consecutive += 1
            tmprow += 1
        tmprow = row
        while tmprow - 1 >= 0 and self.board[tmprow - 1][col] == player:
            consecutive += 1
            tmprow -= 1

        if consecutive >= 4:
            return True

        # Check vertical
        consecutive = 1
        tmpcol = col
        while tmpcol + 1 < GameConstants.COLS and self.board[row][tmpcol + 1] == player:
            consecutive += 1
            tmpcol += 1
        tmpcol = col
        while tmpcol - 1 >= 0 and self.board[row][tmpcol - 1] == player:
            consecutive += 1
            tmpcol -= 1

        if consecutive >= 4:
            return True

        # Check diagonal
        consecutive = 1
        tmprow = row
        tmpcol = col
        while (
            tmprow + 1 < GameConstants.ROWS
            and tmpcol + 1 < GameConstants.COLS
            and self.board[tmprow + 1][tmpcol + 1] == player
        ):
            consecutive += 1
            tmprow += 1
            tmpcol += 1
        tmprow = row
        tmpcol = col
        while (
            tmprow - 1 >= 0
            and tmpcol - 1 >= 0
            and self.board[tmprow - 1][tmpcol - 1] == player
        ):
            consecutive += 1
            tmprow -= 1
            tmpcol -= 1

        if consecutive >= 4:
            return True

        # Check anti-diagonal
        consecutive = 1
        tmprow = row
        tmpcol = col
        while (
            tmprow + 1 < GameConstants.ROWS
            and tmpcol - 1 >= 0
            and self.board[tmprow + 1][tmpcol - 1] == player
        ):
            consecutive += 1
            tmprow += 1
            tmpcol -= 1
        tmprow = row
        tmpcol = col
        while (
            tmprow - 1 >= 0
            and tmpcol + 1 < GameConstants.COLS
            and self.board[tmprow - 1][tmpcol + 1] == player
        ):
            consecutive += 1
            tmprow -= 1
            tmpcol += 1

        if consecutive >= 4:
            return True

        return False

    def game_over(self):
        return self.check_win() or len(self.get_legal_moves()) == 0

    def get_outcome(self):
        if len(self.get_legal_moves()) == 0 and self.check_win() == 0:
            return GameConstants.OUTCOMES["draw"]

        return (
            GameConstants.OUTCOMES["one"]
            if self.check_win() == GameConstants.PLAYERS["one"]
            else GameConstants.OUTCOMES["two"]
        )

    def print(self):
        print("=============================")

        for row in range(GameConstants.ROWS):
            for col in range(GameConstants.COLS):
                print(
                    "| {} ".format(
                        "X"
                        if self.board[row][col] == 1
                        else "O"
                        if self.board[row][col] == 2
                        else " "
                    ),
                    end="",
                )
            print("|")

        print("=============================")
