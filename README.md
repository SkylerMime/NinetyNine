# NinetyNine

University Capstone Project

A computer implementation of the card game Ninety-Nine, invented by David Parlett.  
Includes a GUI created with the Pygame library, and an optional AI opponent.

## How to use

NinetyNine requires Python 3.12. Previous versions may not be supported.

The graphical version of the game requires Pygame, and the
testing module requires Pytest. These libraries can be quickly
installed using the requirements.txt file:

> pip install -r requirements.txt

To run the graphical version of the game, call the module from the NinetyNine directory:

> python3 -m ninety_nine.graphical_main_game

Or call this module for the command line version:

> python3 -m ninety_nine.human_ai_main_game

To run the testing suite:

> pytest .

## Technical Details

### Monte Carlo Tree Search

The AI uses an algorithm called the Monte Carlo
Tree Search. This algorithm works by modeling all the possible game states as
a tree, where each node represents a game state and each edge represents a card that
can be played to enter the next state. In theory, this tree could be fully analyzed
in order to find the best move for any given turn, but in practice the state space is
too large for this to be computationally feasible.

The Monte Carlo Tree Search algorithm gets around this barrier by only searching a subset of the tree.
Specifically, it tries to balance exploration and exploitation by probing a few different paths of
the tree, and fully analyzing the ones that seem most promising.

For more detailed information on the MCTS algorithm, see the citations

> CITATIONS.md

### Further Research

Unfortunately, the algorithm as I have implemented it seems to
perform no better than one which randomly selects moves. With further development, and possibly
a different choice of algorithms, I could get better results.

The algorithm as written now has knowledge of the cards players hold. This is called a Double Dummy
algorithm in computer card terminology, and an ideal algorithm would perform without knowledge
of the other cards in order to put it on an equal level with the human players. After an algorithm
is developed to play the perfect-information game well, this would be the next step.

Some ideas about how this could work, and a detailed problem statement, can be found in the project documents

> project_documents/problem_statement.md

Finally, I have not implemented any bidding engine for the AI -- instead, it chooses its bid randomly.
