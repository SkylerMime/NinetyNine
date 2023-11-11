import pytest

import numpy as np
from experiments import monte_carlo_search_tree as mcst
from experiments import connect_four as game


@pytest.fixture
def three_connected_nodes():
    node1 = mcst.Node(None, None)
    node2 = mcst.Node(1, node1)
    node3 = mcst.Node(4, node2)
    return node3


def test_backpropogate(three_connected_nodes):
    mcst.backpropogate(three_connected_nodes, game.PLAYERS["one"], game.OUTCOMES["one"])

    assert three_connected_nodes.visits == 1 and three_connected_nodes.wins == 1
    assert three_connected_nodes.parent.visits == 1 and three_connected_nodes.parent.wins == 0
    assert (
        three_connected_nodes.parent.parent.visits == 1
        and three_connected_nodes.parent.parent.wins == 1
    )
