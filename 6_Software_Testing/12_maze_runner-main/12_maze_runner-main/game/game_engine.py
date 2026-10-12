import json
import os
import time
import pygame

from game.maze import generate_maze, CELL
from game.player import Player

FPS = 60
BG = (240, 235, 220)
WALL_COLOR = (40, 40, 60)
EXIT_COLOR = (80, 200, 80)
HINT_COLOR = (255, 190, 40)
FOG_COLOR = (10, 10, 20, 238)

DIFFICULTIES = {
    "Easy": (10, 8),
    "Medium": (15, 13),
    "Hard": (20, 18),
}
LEADERBOARD_FILE = "leaderboard.json"
LEADERBOARD_SIZE = 5


def find_shortest_path(walls, start, end, rows, cols):
    """Find a shortest route through the maze using breadth-first search."""
    from collections import deque

    queue = deque([start])
    parent = {start: None}
    # Wall order in game.maze is North, South, East, West.
    directions = [(-1, 0, 0), (1, 0, 1), (0, 1, 2), (0, -1, 3)]
    opposite = [1, 0, 3, 2]

    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            break

        for dr, dc, wall_dir in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if walls[r][c][wall_dir] or walls[nr][nc][opposite[wall_dir]]:
                continue
            nxt = (nr, nc)
            if nxt not in parent:
                parent[nxt] = (r, c)
                queue.append(nxt)

    if end not in parent:
        return []

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    return list(reversed(path))


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20)
        self.small_font = pygame.font.SysFont("monospace", 15)
        self.big_font = pygame.font.SysFont("monospace", 34, bold=True)
        self.difficulty = "Medium"
        self.cols, self.rows = DIFFICULTIES[self.difficulty]
        self.show_hint = False
        self.leaderboard = self.load_leaderboard()
        self.choose_difficulty()
        self.reset()

    def load_leaderboard(self):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                return []
            valid = []
            for item in data:
                if isinstance(item, dict) and isinstance(item.get("time"), (int, float)):
                    valid.append({
                        "difficulty": str(item.get("difficulty", "Medium")),
                        "time": float(item["time"]),
                    })
            return sorted(valid, key=lambda item: item["time"])[:LEADERBOARD_SIZE]
        except (OSError, json.JSONDecodeError):
            return []

    def save_leaderboard(self):
        try:
            with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                json.dump(self.leaderboard, f, indent=2)
        except OSError as exc:
            print(f"Could not save leaderboard: {exc}")

    def add_leaderboard_time(self, elapsed):
        self.leaderboard.append({"difficulty": self.difficulty, "time": round(elapsed, 2)})
        self.leaderboard.sort(key=lambda item: item["time"])
        self.leaderboard = self.leaderboard[:LEADERBOARD_SIZE]
        self.save_leaderboard()

    def choose_difficulty(self):
        options = list(DIFFICULTIES.keys())
        selected = options.index(self.difficulty)
        while True:
            self.screen.fill((30, 30, 50))
            title = self.big_font.render("MAZE RUNNER", True, (245, 245, 245))
            prompt = self.font.render("Choose difficulty", True, (220, 220, 220))
            self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 110))
            self.screen.blit(prompt, (self.screen.get_width() // 2 - prompt.get_width() // 2, 175))

            for i, name in enumerate(options):
                cols, rows = DIFFICULTIES[name]
                color = (255, 190, 40) if i == selected else (220, 220, 220)
                label = self.font.render(f"{'>' if i == selected else ' '} {name}: {cols} x {rows}", True, color)
                self.screen.blit(label, (self.screen.get_width() // 2 - label.get_width() // 2, 235 + i * 45))

            hint = self.small_font.render("UP/DOWN to choose, ENTER to start", True, (190, 190, 200))
            self.screen.blit(hint, (self.screen.get_width() // 2 - hint.get_width() // 2, 410))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % len(options)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % len(options)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.difficulty = options[selected]
                        self.cols, self.rows = DIFFICULTIES[self.difficulty]
                        width = self.cols * CELL
                        height = self.rows * CELL + 70
                        self.screen = pygame.display.set_mode((width, height))
                        return
            self.clock.tick(FPS)

    def reset(self):
        self.walls = generate_maze(self.cols, self.rows)
        self.player = Player(0, 0)
        self.exit_rect = pygame.Rect(
            (self.cols - 1) * CELL + 5,
            (self.rows - 1) * CELL + 5,
            CELL - 10,
            CELL - 10,
        )
        self.start_time = time.time()
        self.elapsed = 0.0
        self.won = False
        self.show_hint = False
        self.score_saved = False

    def player_cell(self):
        col = max(0, min(self.cols - 1, self.player.rect.centerx // CELL))
        row = max(0, min(self.rows - 1, self.player.rect.centery // CELL))
        return row, col

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_h:
                    self.show_hint = not self.show_hint
                elif event.key == pygame.K_ESCAPE and self.won:
                    self.choose_difficulty()
                    self.reset()
        return True

    def update(self):
        if self.won:
            return
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.walls, self.rows, self.cols)
        self.elapsed = time.time() - self.start_time
        if self.player.rect.colliderect(self.exit_rect):
            self.won = True
            if not self.score_saved:
                self.add_leaderboard_time(self.elapsed)
                self.score_saved = True

    def draw_maze(self):
        wall_w = 3
        for r in range(self.rows):
            for c in range(self.cols):
                x, y = c * CELL, r * CELL
                w = self.walls[r][c]
                if w[0]:
                    pygame.draw.line(self.screen, WALL_COLOR, (x, y), (x + CELL, y), wall_w)
                if w[1]:
                    pygame.draw.line(self.screen, WALL_COLOR, (x, y + CELL), (x + CELL, y + CELL), wall_w)
                if w[2]:
                    pygame.draw.line(self.screen, WALL_COLOR, (x + CELL, y), (x + CELL, y + CELL), wall_w)
                if w[3]:
                    pygame.draw.line(self.screen, WALL_COLOR, (x, y), (x, y + CELL), wall_w)

    def draw_fog(self):
        player_r, player_c = self.player_cell()
        radius = 3
        fog = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
        fog.fill(FOG_COLOR)
        for r in range(self.rows):
            for c in range(self.cols):
                # Manhattan distance gives a clear, predictable radius of 3 cells.
                if abs(r - player_r) + abs(c - player_c) > radius:
                    self.screen.blit(fog, (c * CELL, r * CELL))

    def draw_leaderboard(self, center_y):
        title = self.font.render("TOP 5 TIMES", True, (255, 220, 100))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, center_y))
        entries = self.leaderboard[:LEADERBOARD_SIZE]
        if not entries:
            line = self.small_font.render("No completed runs yet", True, (235, 235, 235))
            self.screen.blit(line, (self.screen.get_width() // 2 - line.get_width() // 2, center_y + 30))
            return
        for i, entry in enumerate(entries):
            text = f"{i + 1}. {entry['time']:.2f}s  ({entry['difficulty']})"
            surf = self.small_font.render(text, True, (235, 235, 235))
            self.screen.blit(surf, (self.screen.get_width() // 2 - surf.get_width() // 2, center_y + 28 + i * 22))

    def draw(self):
        self.screen.fill(BG)

        if self.show_hint:
            start = self.player_cell()
            end = (self.rows - 1, self.cols - 1)
            path = find_shortest_path(self.walls, start, end, self.rows, self.cols)
            for r, c in path:
                rect = pygame.Rect(c * CELL + 8, r * CELL + 8, CELL - 16, CELL - 16)
                pygame.draw.rect(self.screen, HINT_COLOR, rect, border_radius=5)

        self.draw_maze()
        self.draw_fog()

        # Exit is visible only when it is within the player's revealed area.
        player_r, player_c = self.player_cell()
        exit_visible = abs((self.rows - 1) - player_r) + abs((self.cols - 1) - player_c) <= 3
        if exit_visible:
            pygame.draw.rect(self.screen, EXIT_COLOR, self.exit_rect, border_radius=4)
            label = self.font.render("EXIT", True, (20, 80, 20))
            self.screen.blit(label, (self.exit_rect.x + 2, self.exit_rect.y + 4))

        self.player.draw(self.screen)

        hud_y = self.rows * CELL
        pygame.draw.rect(self.screen, (30, 30, 50), pygame.Rect(0, hud_y, self.screen.get_width(), 70))
        hud = self.small_font.render(
            f"{self.difficulty} | Time: {self.elapsed:.1f}s | H = Hint | R = New Maze",
            True, (230, 230, 230)
        )
        self.screen.blit(hud, (8, hud_y + 8))

        if self.won:
            overlay = pygame.Surface((self.screen.get_width(), self.rows * CELL), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 175))
            self.screen.blit(overlay, (0, 0))
            msg = self.big_font.render(f"Solved in {self.elapsed:.2f}s!", True, (100, 255, 120))
            self.screen.blit(msg, (self.screen.get_width() // 2 - msg.get_width() // 2, 45))
            self.draw_leaderboard(105)
            sub = self.small_font.render("Press R for a new maze | Close window to quit", True, (235, 235, 235))
            self.screen.blit(sub, (self.screen.get_width() // 2 - sub.get_width() // 2, self.rows * CELL - 28))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
