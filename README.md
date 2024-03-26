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