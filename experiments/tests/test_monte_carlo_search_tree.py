import pytest

import numpy as np
from experiments import mcts as mcst
from experiments import ConnectState as game
from experiments import meta


@pytest.fixture
def three_connected_nodes():
    node1 = mcst.Node(None, None)
    node2 = mcst.Node(1, node1)
    node3 = mcst.Node(4, node2)
    return node3


def test_backpropogate(three_connected_nodes):
    tree_search = mcst.MCTS()

    tree_search.back_propagate(three_connected_nodes, meta.GameMeta.PLAYERS["one"], meta.GameMeta.OUTCOMES["one"])

    assert three_connected_nodes.N == 1 and three_connected_nodes.Q == 0
    assert three_connected_nodes.parent.N == 1 and three_connected_nodes.parent.Q == 1
    assert (
        three_connected_nodes.parent.parent.N == 1
        and three_connected_nodes.parent.parent.Q == 0
    )
