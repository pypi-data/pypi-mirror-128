# bomberman-code-showdown

To install:

```
pip instal .
```

To start the game:

```
code-showdown-bomberman
```

# Playing the game

The purpose of the game is to create an AI that controls the game through HTTP commands.

The URL routes are:

- `GET /player-[i]/game-state` : get a representation of the full game state. Information included: game objects such as
  walls, bombs, other players
- `POST /player-[i]/action`: do something in game
    - `{"action": "move", "direction": "up|down|left|right"}` -> move the current player
    - `{"action": "bomb"}` -> place a bomb