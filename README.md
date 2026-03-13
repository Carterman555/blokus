# Blokus
---
Play Blokus with four players.

## Getting Started
---

### Prerequisites:
- Python 3.6+
- Git

### Setup:

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Clone Repository
```
git clone https://github.com/Carterman555/blokus
cd blokus
```

Run `./run.sh` to open game.

## Playing Blokus:
---

1. Blue goes first.
2. Left click on a piece to begin placing it on the board.
3. Orient the piece.
    - 'a' to rotate it counter clockwise
    - 'd' to rotate it clockwise
    - 's' to reflect it vertically
4. Left click to place the piece when it is in a valid position.
    - [Blokus rules](https://www.wikihow.com/Play-Blokus)
5. The next player can place a piece.
6. Repeat until there are no valid positions for any player.
    - Players who cannot go will automatically be skipped.
7. The player who placed the most total squares wins.