import unittest
from experiments import monteCarloSearchTree as mcst

class TestNode(unittest.TestCase):

    def setUp(self):
        self.root = mcst.Node(None, [], None)
        self.child = mcst.Node(self.root, [], None)
        self.root.children.append(self.child)
        
    def test_isNonTerminal(self):
        self.assertTrue(self.root.isNonTerminal())
        self.assertFalse(self.child.isNonTerminal())

if __name__ == '__main__':
    unittest.main()