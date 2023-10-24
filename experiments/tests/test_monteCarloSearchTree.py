import unittest
import math, random
from experiments import monteCarloSearchTree as mcst
from experiments import connectFour as game

class TestNode(unittest.TestCase):

    def setUp(self):
        self.root = mcst.Node(None)
        self.child = mcst.Node(self.root)
        self.winningChild = mcst.Node(self.root)
        self.losingChild = mcst.Node(self.root)
        self.root.children.append(self.winningChild)

        self.root.visits = 4

        self.winningChild.visits = 12
        self.winningChild.wins = 7
        self.winningChild.losses = 3
        self.winningChild.draws = 2

        self.losingChild.visits = 17
        self.losingChild.wins = 6
        self.losingChild.losses = 7
        self.losingChild.draws = 4

    def test_updateStats(self):
        self.child.updateStats(1)
        self.assertTrue(self.child.wins == 1)
        self.assertTrue(self.child.losses == 0)
        self.assertTrue(self.child.draws == 0)

    def test_isRoot(self):
        self.assertTrue(self.root.isRoot())
        self.assertFalse(self.child.isRoot())
    
    def test_meanValue(self):
        self.assertEqual(self.winningChild.getMeanValue(), 1/3)
        self.assertEqual(self.losingChild.getMeanValue(), -1/17)

    def test_ucb(self):
        self.assertEqual(self.winningChild.getUcb(), 1/3+mcst.UCB_CONSTANT*math.sqrt(math.log(4)/12))
        self.assertEqual(self.losingChild.getUcb(), -1/17+mcst.UCB_CONSTANT*math.sqrt(math.log(4)/17))



class TestConnectFour(unittest.TestCase):

    def setUp(self):
        self.rootBoard = game.newBoard()
        self.rootBoard = game.makeMove("O", 3, self.rootBoard)
        self.root = mcst.ConnectFourNode(None, self.rootBoard, 3, "O")
        
        # initialize randomness for reproducibility
        random.seed(300)
        self.initialState = random.getstate()
        random.setstate(self.initialState)

    def test_createUnexploredChild_OfRoot(self):
       # Manual creation (for comparison)
       colToDropIn = random.choice([0, 1, 2, 4, 5, 6])
       newChildComparisonBoard = game.makeMove("X", colToDropIn, self.rootBoard)
       newChildComparison = mcst.ConnectFourNode(self.root, newChildComparisonBoard, colToDropIn, "X")
       # Method creation
       random.setstate(self.initialState)
       newChild = self.root.createUnexploredChild()
       
       self.assertEqual(newChild.boardState, newChildComparison.boardState)

    def test_manuallyAddChildren(self):
        self.childBoard = self.rootBoard.copy()
        self.childBoard = game.makeMove("X", 3, self.childBoard)
        self.child = mcst.ConnectFourNode(self.root, self.childBoard, 3, "X")
        self.root.children.append(self.child)

        self.root.createUnexploredChild()

        self.assertEqual(len(self.root.children), 2)

    def test_createAllTheChildren_throwsError(self):
        for i in range(game.NUM_COLUMNS):
            self.root.createUnexploredChild()
        # there are no other unexplored children
        with self.assertRaises(IndexError):
            self.root.createUnexploredChild()

    def test_fillingAColumn_UnexploredChildrenWillYield(self):
        fullTestBoard = [
            ['_', 'O', '_', '_', '_', 'O', 'X'],
            ['_', 'X', '_', '_', '_', 'X', 'O'],
            ['O', 'O', '_', '_', 'X', 'X', 'O'],
            ['X', 'X', 'X', 'O', 'O', 'O', 'X'],
            ['O', 'O', 'X', 'X', 'O', 'X', 'O'],
            ['X', 'X', 'O', 'X', 'O', 'O', 'X']
        ]
        self.root = mcst.ConnectFourNode(None, fullTestBoard, 0, "O")
        self.root.createUnexploredChild()




if __name__ == '__main__':
    unittest.main()