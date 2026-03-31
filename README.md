# 🗡️ Dungeon Crawler

A terminal-based roguelike dungeon crawler built in Python. Fully playable with real-time input, procedural dungeons, combat, and loot — no external dependencies required.

<img width="569" height="509" alt="image" src="https://github.com/user-attachments/assets/94daba8e-081e-4ef0-8cd1-4d7ce6b61317" />
<img width="689" height="375" alt="image" src="https://github.com/user-attachments/assets/1f35f51d-5adf-4641-acc5-2a0db1dfc87a" />
<img width="720" height="413" alt="image" src="https://github.com/user-attachments/assets/ecc12b18-d124-43a7-bd4d-58118edfab58" />


---

## Demo

```
############################################################
##..........################################################
##..........##.......#######################################
##...@......##...E...####.......$....####...................
##..........##.......####.........!..####...................
############.....##################..####...................
#########............................####......>............
#########............................####...................
############################################################

Move: W A S D | Quit: Q | Potion: P | Weapon: Fists
HP: [##########] | Score: 0
Inventory: Empty
```

`@` = Player | `E` = Enemy | `$` = Gold | `!` = Potion | `/` = Sword | `>` = Stairs | `#` = Wall

---

## Features

- **Procedural dungeon generation** — 30 rooms carved into a 60x30 grid, connected by L-shaped corridors every run
- **Real-time input** — built with Python's `curses` library, no Enter key required, zero flicker
- **Color coded map** — player in cyan, enemies in red, gold in yellow, potions in green, stairs in magenta
- **Enemy AI** — greedy pathfinding moves enemies toward the player using Manhattan distance
- **Turn-based enemy speed** — enemies move every 2 player turns, keeping the game tactical
- **Combat system** — walk into enemies to attack, they deal damage when they reach you
- **Loot system** — weighted item spawning (gold most common, swords rare, capped at 2 per dungeon)
- **Inventory** — pick up and carry health potions, use them with `P`
- **Sword** — doubles attack damage from 1 to 2 hits per turn
- **HP bar + score** — live HUD showing health, score, weapon, and inventory
- **Game over screen** — ASCII art displayed on death or quit with final score
- **Win screen** — reach the stairs (`>`) to win

---

## How to Run

**Requirements:** Python 3.8+ (no installs needed — `curses` is built into Python on Mac/Linux)

```bash
# Clone the repo
git clone https://github.com/alexddelaney/Dungeon-Game-.git
cd Dungeon-Game-

# Run the game
python3 game.py
```

**Controls:**

| Key | Action |
|-----|--------|
| `W` or `↑` | Move up |
| `S` or `↓` | Move down |
| `A` or `←` | Move left |
| `D` or `→` | Move right |
| `P` | Use health potion |
| `Q` | Quit |

---

## Tuning the Game

All gameplay values are constants at the top of `game.py` — no need to dig into logic to tweak things:

```python
NUM_ROOMS = 30        # More rooms = denser map
NUM_ENEMIES = 5       # Enemies per dungeon
ENEMY_SPEED = 2       # Higher = slower enemies
ENEMY_HP = 3          # Hits to kill an enemy
SWORD_DAMAGE = 2      # Damage with sword
POTION_HEAL = 3       # HP restored per potion
SCORE_KILL = 10       # Points per kill
SCORE_GOLD = 5        # Points per gold coin
```

---

## How It Works

### Map Generation
A 60x30 grid is filled entirely with walls. 30 randomly sized rooms are carved out and their center points stored. L-shaped corridors are then carved between every consecutive pair of room centers, guaranteeing the dungeon is always fully connected and explorable.

### Rendering
Python's built-in `curses` library draws characters directly at exact `(x, y)` coordinates instead of printing full rows. This means only changed cells update each frame — no clearing, no flicker, instant response to input.

### Item System
Items live in a dictionary keyed by `(x, y)` position. Checking whether a tile holds an item is O(1) — instant regardless of how many items exist. When the player steps on a tile, `dict.pop()` removes the item from the map and returns it in one operation.

### Enemy AI
Each enemy calculates the horizontal and vertical distance to the player (`dx`, `dy`). It tries to move in whichever direction closes the larger gap first. If that tile is a wall, it tries the other axis. This greedy approach produces natural-feeling chase behavior without complex pathfinding.

### Combat
Walking into an enemy attacks it instead of moving. Damage is determined by whether the player holds a sword (`SWORD_DAMAGE`) or not (`FIST_DAMAGE`). After every `ENEMY_SPEED` player turns, all enemies move one step. Any enemy sharing a tile with the player deals 1 damage.

---

## What I Learned

- **2D arrays** — representing and manipulating a grid-based map
- **Dictionaries** — O(1) item lookups by position instead of scanning a list
- **OOP** — `Item` and `Enemy` classes with attributes and state
- **Procedural generation** — room carving and corridor algorithms
- **Greedy pathfinding** — Manhattan distance based enemy movement
- **Terminal rendering** — real-time display with Python's `curses` library
- **Game loop design** — turn tracking, state management, win/lose conditions

---

## Author

**Alexander Delaney** — CS Freshman, Louisiana State University  
Built as a portfolio project to apply Python, OOP, and algorithms hands-on.
