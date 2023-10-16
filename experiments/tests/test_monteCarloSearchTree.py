import unittest
import math
from experiments import monteCarloSearchTree as mcst
from experiments import connectFour as game

class TestNode(unittest.TestCase):

    def setUp(self):
        self.root = mcst.Node(None, [], mcst.Stats())
        self.child = mcst.Node(self.root, [], mcst.Stats())
        self.root.children.append(self.child)

    def test_updateStats(self):
        self.child.updateStats(1)
        self.assertTrue(self.child.stats.wins == 1)
        self.assertTrue(self.child.stats.losses == 0)
        self.assertTrue(self.child.stats.draws == 0)

    def test_isRoot(self):
        self.assertTrue(self.root.isRoot())
        self.assertFalse(self.child.isRoot())

class TestStats(unittest.TestCase):

    def setUp(self):
        self.winningTestStats = mcst.Stats()
        self.winningTestStats.visits = 12
        self.winningTestStats.wins = 7
        self.winningTestStats.losses = 3
        self.winningTestStats.draws = 2
        self.winningTestStats.updateMeanValue()
        self.winningTestStats.updateUcb(4)

        self.losingTestStats = mcst.Stats()
        self.losingTestStats.visits = 17
        self.losingTestStats.wins = 6
        self.losingTestStats.losses = 7
        self.losingTestStats.draws = 4
        self.losingTestStats.updateMeanValue()
        self.losingTestStats.updateUcb(5)

    def test_updateMeanValue(self):
        self.assertEqual(self.winningTestStats.meanValue, 1/3)
        self.assertEqual(self.losingTestStats.meanValue, -1/17)

    def test_updateUcb(self):
        self.assertEqual(self.winningTestStats.ucb, 1/3+mcst.UCB_CONSTANT*math.sqrt(math.log(4)/12))
        self.assertEqual(self.losingTestStats.ucb, -1/17+mcst.UCB_CONSTANT*math.sqrt(math.log(5)/17))

class TestConnectFour(unittest.TestCase):

    def setUp(self):
        self.board = game.newBoard()
        game.makeMove("O", 3, self.board)
        self.root = mcst.ConnectFour(None, [], mcst.Stats(), self.board, 3, "O")
        game.makeMove("X", 3, self.board)
        self.child = mcst.Node(self.root, [], mcst.Stats(), self.board, 3, "X")
        self.root.children.append(self.child)



if __name__ == '__main__':
    unittest.main()