import unittest
from experiments import connectFour as game

class TestBoardSetup(unittest.TestCase):

    def setUp(self):
        # Set up a board with no pieces yet
        self.board0 = game.newBoard()

        # Set up a board with one piece in the lower right
        self.board1 = game.newBoard()
        self.board1[game.NUM_ROWS - 1][game.NUM_COLUMNS - 1] = 'X'

        # Set up a board with two pieces in the lower right for comparison
        self.board2 = game.newBoard()
        self.board2[game.NUM_ROWS - 1][game.NUM_COLUMNS - 1] = 'X'
        self.board2[game.NUM_ROWS - 2][game.NUM_COLUMNS - 1] = 'O'

        # board with a column full of 'X's
        self.fullColBoard = game.newBoard()
        for row in range(game.NUM_ROWS):
            self.fullColBoard[row][2] = 'X'

        # board with a column with four 'O's
        self.winOBoard = game.newBoard()
        self.winOBoard[game.NUM_ROWS - 1][3] = 'X'
        for row in range(game.NUM_ROWS - 5, game.NUM_ROWS - 1):
            self.winOBoard[row][3] = 'O'

        # board with a diagonal with four 'X's
        self.winXBoard = game.newBoard()
        self.comparisonBoard = game.newBoard()
        self.comparisonBoard[game.NUM_ROWS - 1][0] = 'X'
        self.comparisonBoard[game.NUM_ROWS - 1][1] = 'O'
        self.comparisonBoard[game.NUM_ROWS - 2][1] = 'X'

    def test_makeMove(self):
        game.makeMove('X', game.NUM_COLUMNS - 1, self.board0)
        self.assertEqual(self.board0, self.board1, 'wrong board after adding to an empty board')
    
        game.makeMove('O', game.NUM_COLUMNS - 1, self.board1)
        self.assertEqual(self.board1, self.board2, 'wrong board after adding to a column with an X')

        game.makeMove('X', 0, self.winXBoard)
        game.makeMove('O', 1, self.winXBoard)
        game.makeMove('X', 1, self.winXBoard)

        self.assertEqual(self.winXBoard, self.comparisonBoard, 'wrong board after three moves')

        with self.assertRaises(ValueError):
            game.makeMove('O', game.NUM_COLUMNS, self.board1)
        with self.assertRaises(ValueError):
            game.makeMove('O', 2, self.fullColBoard)
            
    def test_hasWon(self):
        self.assertTrue(game.hasWon('O', self.winOBoard))
        self.assertFalse(game.hasWon('X', self.winOBoard))

        # board with diagonal 'X' win
        self.winXBoard = game.newBoard()
        game.makeMove('X', 0, self.winXBoard)
        game.makeMove('O', 1, self.winXBoard)
        game.makeMove('X', 1, self.winXBoard)
        game.makeMove('O', 2, self.winXBoard)
        game.makeMove('O', 2, self.winXBoard)
        game.makeMove('X', 2, self.winXBoard)
        game.makeMove('O', 3, self.winXBoard)
        game.makeMove('O', 3, self.winXBoard)
        game.makeMove('O', 3, self.winXBoard)
        game.makeMove('X', 3, self.winXBoard)
        print(self.winXBoard)

        self.assertTrue(game.hasWon('X', self.winXBoard))
        self.assertFalse(game.hasWon('O', self.winXBoard))

if __name__ == '__main__':
    unittest.main()