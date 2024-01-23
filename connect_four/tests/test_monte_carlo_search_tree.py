import pytest

from connect_four import constants, monte_carlo_tree_search as mcst


@pytest.fixture
def three_connected_nodes():
    node1 = mcst.Node(None, None)
    node2 = mcst.Node(1, node1)
    node3 = mcst.Node(4, node2)
    return node3


@pytest.fixture
def tree_search():
    return mcst.MCTS()


def test_backpropogate(three_connected_nodes, tree_search):
    mcst.back_propagate(
        three_connected_nodes,
        constants.GameConstants.PLAYERS["one"],
        constants.GameConstants.OUTCOMES["one"],
    )

    assert three_connected_nodes.visits == 1 and three_connected_nodes.wins == 0
    assert (
        three_connected_nodes.parent.visits == 1
        and three_connected_nodes.parent.wins == 1
    )
    assert (
        three_connected_nodes.parent.parent.visits == 1
        and three_connected_nodes.parent.parent.wins == 0
    )