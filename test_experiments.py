import unittest
from experiments import monteCarloSearchTree as mcst

class TestBoardSetup(unittest.TestCase):

    def setUp(self):
        # Set up a board with no pieces yet
        self.board0 = mcst.newBoard()

        # Set up a board with one piece in the lower right
        self.board1 = mcst.newBoard()
        self.board1[mcst.NUM_ROWS - 1][mcst.NUM_COLUMNS - 1] = 'X'

        # Set up a board with two pieces in the lower right for comparison
        self.board2 = mcst.newBoard()
        self.board2[mcst.NUM_ROWS - 1][mcst.NUM_COLUMNS - 1] = 'X'
        self.board2[mcst.NUM_ROWS - 2][mcst.NUM_COLUMNS - 1] = 'O'

        # board with a column full of 'X's
        self.fullColBoard = mcst.newBoard()
        for row in range(mcst.NUM_ROWS):
            self.fullColBoard[row][2] = 'X'

        # board with a column with four 'O's
        self.winOBoard = mcst.newBoard()
        self.winOBoard[mcst.NUM_ROWS - 1][3] = 'X'
        for row in range(mcst.NUM_ROWS - 5, mcst.NUM_ROWS - 1):
            self.winOBoard[row][3] = 'O'

        # board with a diagonal with four 'X's
        self.winXBoard = mcst.newBoard()
        self.comparisonBoard = mcst.newBoard()
        self.comparisonBoard[mcst.NUM_ROWS - 1][0] = 'X'
        self.comparisonBoard[mcst.NUM_ROWS - 1][1] = 'O'
        self.comparisonBoard[mcst.NUM_ROWS - 2][1] = 'X'

    def test_makeMove(self):
        mcst.makeMove('X', mcst.NUM_COLUMNS - 1, self.board0)
        self.assertEqual(self.board0, self.board1, 'wrong board after adding to an empty board')
    
        mcst.makeMove('O', mcst.NUM_COLUMNS - 1, self.board1)
        self.assertEqual(self.board1, self.board2, 'wrong board after adding to a column with an X')

        mcst.makeMove('X', 0, self.winXBoard)
        mcst.makeMove('O', 1, self.winXBoard)
        mcst.makeMove('X', 1, self.winXBoard)

        self.assertEqual(self.winXBoard, self.comparisonBoard, 'wrong board after three moves')

        with self.assertRaises(ValueError):
            mcst.makeMove('O', mcst.NUM_COLUMNS, self.board1)
        with self.assertRaises(ValueError):
            mcst.makeMove('O', 2, self.fullColBoard)
            
    def test_hasWon(self):
        self.assertTrue(mcst.hasWon('O', self.winOBoard))
        self.assertFalse(mcst.hasWon('X', self.winOBoard))

        # board with diagonal 'X' win
        self.winXBoard = mcst.newBoard()
        mcst.makeMove('X', 0, self.winXBoard)
        mcst.makeMove('O', 1, self.winXBoard)
        mcst.makeMove('X', 1, self.winXBoard)
        mcst.makeMove('O', 2, self.winXBoard)
        mcst.makeMove('O', 2, self.winXBoard)
        mcst.makeMove('X', 2, self.winXBoard)
        mcst.makeMove('O', 3, self.winXBoard)
        mcst.makeMove('O', 3, self.winXBoard)
        mcst.makeMove('O', 3, self.winXBoard)
        mcst.makeMove('X', 3, self.winXBoard)
        print(self.winXBoard)

        self.assertTrue(mcst.hasWon('X', self.winXBoard))
        self.assertFalse(mcst.hasWon('O', self.winXBoard))

if __name__ == '__main__':
    unittest.main()