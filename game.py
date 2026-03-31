import curses
import random

# --- Constants ---
MAP_WIDTH = 40
MAP_HEIGHT = 20
WALL = '#'
FLOOR = '.'
PLAYER = '@'

# --- Item class ---


class Item:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

# --- Enemy class ---


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 3

# --- Build a random map ---


def generate_map():
    grid = [[WALL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    rooms = []

    for _ in range(8):
        room_w = random.randint(4, 10)
        room_h = random.randint(3, 6)
        start_x = random.randint(1, MAP_WIDTH - room_w - 1)
        start_y = random.randint(1, MAP_HEIGHT - room_h - 1)

        for y in range(start_y, start_y + room_h):
            for x in range(start_x, start_x + room_w):
                grid[y][x] = FLOOR

        center_x = start_x + room_w // 2
        center_y = start_y + room_h // 2
        rooms.append((center_x, center_y))

    for i in range(len(rooms) - 1):
        x1, y1 = rooms[i]
        x2, y2 = rooms[i + 1]

        for x in range(min(x1, x2), max(x1, x2) + 1):
            grid[y1][x] = FLOOR
        for y in range(min(y1, y2), max(y1, y2) + 1):
            grid[y][x2] = FLOOR

    return grid

# --- Find a valid starting spot for the player ---


def find_start(grid):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if grid[y][x] == FLOOR:
                return x, y

# --- Place items randomly on floor tiles ---


def place_items(grid):
    items = {}

    item_types = [
        Item("Gold Coin", "$"),
        Item("Health Potion", "!"),
    ]

    attempts = 0
    placed = 0
    while placed < 10 and attempts < 200:
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)
        if grid[y][x] == FLOOR and (x, y) not in items:
            template = random.choice(item_types)
            items[(x, y)] = Item(template.name, template.symbol)
            placed += 1
        attempts += 1

    return items

# --- Places enemies randomly on floor tiles ---


def place_enemies(grid):
    enemies = []
    attempts = 0
    placed = 0
    while placed < 5 and attempts < 200:
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)
        if grid[y][x] == FLOOR:
            enemies.append(Enemy(x, y))
            placed += 1
        attempts += 1
    return enemies

# --- Move each enemy one step toward the player ---


def move_enemies(enemies, px, py, grid):
    for enemy in enemies:
        dx = px - enemy.x
        dy = py - enemy.y

        # Try to close the larger gap first
        moves = []
        if abs(dx) >= abs(dy):
            moves = [(dx, 0), (0, dy)]
        else:
            moves = [(0, dy), (dx, 0)]

        for mx, my in moves:
            if mx == 0 and my == 0:
                continue
            # Normalize to one step
            step_x = (1 if mx > 0 else -1) if mx != 0 else 0
            step_y = (1 if my > 0 else -1) if my != 0 else 0
            nx = enemy.x + step_x
            ny = enemy.y + step_y
            if grid[ny][nx] == FLOOR:
                enemy.x = nx
                enemy.y = ny
                break


# --- Game over screen ---


def show_game_over(stdscr, score):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    lines = [
        "  ____    _    __  __ _____    _____     _______ ____  ",
        " / ___|  / \\  |  \\/  | ____|  / _ \\ \\   / / ____|  _ \\ ",
        "| |  _  / _ \\ | |\\/| |  _|   | | | \\ \\ / /|  _| | |_) |",
        "| |_| |/ ___ \\| |  | | |___  | |_| |\\ V / | |___|  _ < ",
        " \\____/_/   \\_\\_|  |_|_____|  \\___/  \\_/  |_____|_| \\_\\",
    ]
    start_y = h // 2 - len(lines) // 2 - 2
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(start_y + i, max(0, w // 2 - len(line) // 2), line,
                          curses.color_pair(1))
        except curses.error:
            pass
    try:
        score_text = f"Final Score: {score}"
        stdscr.addstr(start_y + len(lines) + 2, w // 2 - len(score_text) // 2,
                      score_text, curses.color_pair(2))
        quit_text = "Press any key to quit..."
        stdscr.addstr(start_y + len(lines) + 4, w // 2 - len(quit_text) // 2,
                      quit_text, curses.color_pair(5))
    except curses.error:
        pass
    stdscr.refresh()
    stdscr.getch()


def draw(stdscr, grid, px, py, items, inventory, enemies, player_hp, score):
    max_y, max_x = stdscr.getmaxyx()

    enemy_positions = {(e.x, e.y) for e in enemies}
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if y < max_y and x < max_x:
                if x == px and y == py:
                    ch = PLAYER
                    color = curses.color_pair(4)
                elif (x, y) in enemy_positions:
                    ch = 'E'
                    color = curses.color_pair(1)
                elif (x, y) in items:
                    ch = items[(x, y)].symbol
                    color = curses.color_pair(
                        2) if ch == '$' else curses.color_pair(3)
                else:
                    ch = grid[y][x]
                    color = curses.color_pair(5)
                try:
                    stdscr.addch(y, x, ch, color)
                except curses.error:
                    pass

    try:
        stdscr.addstr(MAP_HEIGHT + 1, 0,
                      "Move: W A S D | Quit: Q | Use Potion: P")
    except curses.error:
        pass

    try:
        hp_bar = "HP: [" + "#" * player_hp + "." * (10 - player_hp) + "]"
        stdscr.addstr(MAP_HEIGHT + 2, 0, hp_bar + " | Score: " + str(score))
    except curses.error:
        pass

    try:
        inv_text = "Inventory: " + \
            (", ".join(i.name for i in inventory) if inventory else "Empty")
        stdscr.addstr(MAP_HEIGHT + 3, 0, inv_text)
    except curses.error:
        pass

    stdscr.refresh()

# --- Main game loop ---


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    grid = generate_map()
    px, py = find_start(grid)
    items = place_items(grid)
    enemies = place_enemies(grid)
    inventory = []
    turn = 0
    player_hp = 10
    score = 0

    while True:
        if player_hp <= 0:
            show_game_over(stdscr, score)
            break
        draw(stdscr, grid, px, py, items, inventory, enemies, player_hp, score)
        key = stdscr.getch()

        # Use Q key in order to quit the game
        if key in (ord('q'), ord('Q')):
            show_game_over(stdscr, score)
            break

        # Use Health Potions with P key
        if key in (ord('p'), ord('P')):
            for i, item in enumerate(inventory):
                if item.name == "Health Potion":
                    player_hp = min(10, player_hp + 3)
                    inventory.pop(i)
                    break

        nx, ny = px, py
        if key in (ord('w'), ord('W'), curses.KEY_UP):
            ny -= 1
        elif key in (ord('s'), ord('S'), curses.KEY_DOWN):
            ny += 1
        elif key in (ord('a'), ord('A'), curses.KEY_LEFT):
            nx -= 1
        elif key in (ord('d'), ord('D'), curses.KEY_RIGHT):
            nx += 1

        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            # Check if an enemy is at the target tile
            target_enemy = None
            for e in enemies:
                if e.x == nx and e.y == ny:
                    target_enemy = e
                    break

            if target_enemy:
                # Attack the enemy instead of moving
                target_enemy.hp -= 1
                if target_enemy.hp <= 0:
                    enemies.remove(target_enemy)
                    score += 10
            elif grid[ny][nx] == FLOOR:
                px, py = nx, ny
                if (px, py) in items:
                    picked = items.pop((px, py))
                    inventory.append(picked)
                    if picked.name == "Gold Coin":
                        score += 5

        turn += 1
        if turn % 2 == 0:
            move_enemies(enemies, px, py, grid)
            # Check if any enemy is standing on the player
            for e in enemies:
                if e.x == px and e.y == py:
                    player_hp -= 1


'''
items.pop takes object from the map puts it in inentory and removes it from 
the map.
'''


# --- Entry point ---
curses.wrapper(main)
