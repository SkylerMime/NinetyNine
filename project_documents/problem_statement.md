# Double Dummy Solver

The first step to improving my solver is to implement a strong 'Double Dummy Solver'.
The term comes from Computer Bridge, and simply refers to an AI that chooses moves based on perfect
information of the cards held by the other two players. So unlike in the real game, player's hands will
not be hidden from the AI. From there, I can build up to an AI without perfect knowledge of the hands.

## Problem Statement

Ninety Nine is a trick-taking card game with three players. Trick-taking means the game is split up into nine
minigames called "tricks" where each player plays one card,
and each trick will have exactly one winner who is said to "capture" the trick.

At the beginning of the playing phase of the game, each of the three players will have nine cards in hand
from a deck of 36 cards, ranked 6-A and in four suits. Each player will also have chosen a Bid Value which
represents the exact amount of tricks they plan on capturing, and the game will have a designated trump
suit that can beat cards from the other three suits.

The AI will be one of these players, and its goal is to capture EXACTLY as many tricks as it bids. In theory
it should be able to do this given any initial starting hand distribution, but the first step will be to develop
and test it for one specific hand distribution, and one chosen trump suit (Clubs),
and each player's bid value will be "3", meaning they are trying to capture exactly three tricks.
If the AI can achieve this goal on average more often than players making purely
random choices, it will be a vast improvement.

### Detailed turn order

- The AI will start by playing any card to the first trick.
This is called the "led card," and its suit is the "led suit."
- In clockwise order each other player will play a card to the table where:
    - The card's suit be the same as the led suit if possible.
    - If the player does not have any cards of the led suit, they may play any card.
- The winner of the trick is:
  - Whoever played the highest card in the trump suit, if any were played.
  - Whoever played the highest card in the led suit, if no trump cards were played.
- Whoever won the previous trick will lead a new card to start the next trick.
- After all cards are played, all players who captured exactly three tricks earn points.

If on average the AI earns more points than either opponent, it has succeeded.

### The state space of Ninety Nine

Ninety Nine uses 36 unique cards, ranked Six through Ace in four suits. These cards are thoroughly
dealt out to each player, resulting in (36 choose 12) * (24 choose 12) possible hand distributions, or 3*10^15.

From this point, each player sets aside three cards as a bid, which means (12 choose 3)^3
possible initial hand/bid distributions.

This is the point where the double-dummy solver begins, and since not every card is legal to play,
the exact state space for the rest of the game is difficult to determine. The upper bound would be if
every card were legal to play every time, meaning that for each of nine tricks every player can choose any one of their
nine hand cards to play: (9!)^3 possible orders of play, or 5*10^16.
