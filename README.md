# NinetyNine

University Capstone Project

AI to play the card game Ninety-Nine (invented by David Parlett)

## How to use

Ninety-Nine requires Python 3.12.

The graphical version of the game requires Pygame, and the
testing module requires Pytest. These libraries can be quickly
installed using the requirements.txt file:

> pip install -r requirements.txt

To run the graphical version of the game:

> python3 ninety_nine/graphical_main_game.py

Or the command line version:

> python3 ninety_nine/human_ai_main_game.py

To run the testing suite:

> pytest .

## Development history

My first attempt at creating the AI used an algorithm called the Monte Carlo
Tree Search, but the results were disappointing. The algorithm ran slowly, and
performed no better than randomly selecting moves. I was convinced I could get
better performance, and decided to focus on a double-dummy solver, a solver
that can always find the optimal move given the current state of the game (including
all player's hands). I also decided to pass over the bidding stage, stipulating
that the computer always bid three.

## The state space of Ninety Nine

Ninety Nine uses 36 unique cards, ranked Six through Ace in four suits. These cards are thoroughly
dealt out to each player, resulting in (36 choose 12) * (24 choose 12) possible hand distributions, or 3*10^15.

From this point, each player sets aside three cards as a bid, which means (12 choose 3)^3
possible initial hand/bid distributions.

This is the point where the double-dummy solver begins, and since not every card is legal to play,
the exact state space for the rest of the game is difficult to determine. The upper bound would be if
every card were legal to play every time, meaning that for each of nine tricks every player can choose any one of their
nine hand cards to play: (9!)^3 possible orders of play, or 5*10^16.

## The double-dummy solver

For more in-depth information on this stage of development and testing, see
> project_documents/double_dummy_solver.md