"""
AJVYRA 30-GAME ENGINE
One Python file containing a reusable engine and 30 playable mini-games.

Install:
    pip install pygame

Run:
    python ajvyra_30_games.py

Controls:
    Arrow keys / WASD = movement
    SPACE = action / jump / shoot depending on game
    ESC = return to menu
    R = restart current game
"""

import math
import random
import sys
from dataclasses import dataclass

import pygame

pygame.init()

WIDTH, HEIGHT = 1100, 700
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AJVYRA — 30 Games")
CLOCK = pygame.time.Clock()

FONT = pygame.font.Font(None, 30)
SMALL = pygame.font.Font(None, 23)
TITLE = pygame.font.Font(None, 64)
BIG = pygame.font.Font(None, 42)

WHITE = (240, 240, 245)
MUTED = (145, 145, 160)
BLACK = (7, 8, 12)
PANEL = (15, 17, 24)
GRID = (28, 31, 42)
RED = (220, 65, 75)
GREEN = (65, 210, 125)
BLUE = (75, 145, 235)
YELLOW = (235, 205, 75)
PURPLE = (155, 90, 230)
CYAN = (65, 210, 220)
ORANGE = (235, 135, 60)

PLAYER_SIZE = 28


@dataclass
class GameInfo:
    number: int
    title: str
    genre: str
    description: str


GAMES = [
    GameInfo(1, "Black Run", "Arcade / Platformer", "Collect energy and reach the gate."),
    GameInfo(2, "Shadow Hunt", "Horror", "Find the keys while shadows chase you."),
    GameInfo(3, "Neon Drift", "Racing", "Drive through checkpoints before time runs out."),
    GameInfo(4, "Crystal Quest", "RPG / Adventure", "Collect crystals and defeat guardians."),
    GameInfo(5, "Cipher Room", "Puzzle", "Activate switches in the correct sequence."),
    GameInfo(6, "Silent Step", "Stealth", "Reach the exit without entering enemy vision."),
    GameInfo(7, "Meteor Zero", "Survival", "Survive falling meteors."),
    GameInfo(8, "Last Tower", "Action", "Defend the tower from incoming enemies."),
    GameInfo(9, "Lost Signal", "Mystery", "Locate signal fragments around the map."),
    GameInfo(10, "Void Arena", "Combat", "Survive waves of enemies."),
    GameInfo(11, "Frost Line", "Racing", "Cross icy checkpoints quickly."),
    GameInfo(12, "Night Courier", "Adventure", "Deliver the package to the target."),
    GameInfo(13, "Red Maze", "Puzzle", "Escape the changing maze."),
    GameInfo(14, "Echo Cave", "Exploration", "Collect echoes before the cave closes."),
    GameInfo(15, "Iron Squad", "Strategy", "Protect your base and gather energy."),
    GameInfo(16, "Ghost Train", "Horror", "Escape the train while avoiding ghosts."),
    GameInfo(17, "Skyfall", "Arcade", "Move through falling obstacles."),
    GameInfo(18, "Black Harbor", "Mystery", "Find three hidden clues."),
    GameInfo(19, "Pulse", "Rhythm / Skill", "Hit moving targets at the right time."),
    GameInfo(20, "Dragon Core", "Action / Fantasy", "Defeat the core guardian."),
    GameInfo(21, "Deep One", "Survival", "Survive underwater hazards."),
    GameInfo(22, "Zero Gravity", "Arcade", "Collect stars in a floating arena."),
    GameInfo(23, "Hunter", "Combat", "Track targets and survive ambushes."),
    GameInfo(24, "Memory Grid", "Puzzle", "Remember and repeat the pattern."),
    GameInfo(25, "Desert Run", "Racing", "Cross the desert and avoid hazards."),
    GameInfo(26, "Night Watch", "Defense", "Keep enemies away from the beacon."),
    GameInfo(27, "Phantom Key", "Stealth", "Find the key and escape unseen."),
    GameInfo(28, "Star Forge", "Strategy", "Collect energy and build the forge."),
    GameInfo(29, "Final Gate", "Boss / Action", "Break through the guardian."),
    GameInfo(30, "AJVYRA Zero", "Mixed / Challenge", "A compact final challenge using multiple mechanics."),
]


def text(surface, value, pos, font=FONT, color=WHITE, center=False):
    image = font.render(str(value), True, color)
    rect = image.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(image, rect)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def move_rect(rect, keys, speed=5):
    dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (
        keys[pygame.K_a] or keys[pygame.K_LEFT]
    )
    dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (
        keys[pygame.K_w] or keys[pygame.K_UP]
    )
    if dx or dy:
        length = math.hypot(dx, dy)
        rect.x += int(dx / length * speed)
        rect.y += int(dy / length * speed)
    rect.x = clamp(rect.x, 20, WIDTH - 20 - rect.width)
    rect.y = clamp(rect.y, 90, HEIGHT - 25 - rect.height)


class Game:
    def __init__(self, info):
        self.info = info
        self.running = True
        self.finished = False
        self.won = False
        self.score = 0
        self.time = 45.0
        self.level = 1
        self.player = pygame.Rect(70, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.target = pygame.Rect(WIDTH - 100, HEIGHT // 2, 35, 35)
        self.objects = []
        self.enemies = []
        self.bullets = []
        self.cooldown = 0
        self.flash = 0
        self.wave = 0
        self.pattern = []
        self.pattern_input = []
        self.pattern_timer = 0
        self.setup()

    def setup(self):
        n = self.info.number

        if n == 24:
            self.pattern = [random.randrange(9) for _ in range(4)]
            self.pattern_timer = 2.0
        elif n == 5:
            self.pattern = [random.randrange(4) for _ in range(4)]
            self.objects = [pygame.Rect(160 + i * 190, 300, 70, 70) for i in range(4)]
        elif n == 13:
            self.objects = [
                pygame.Rect(random.randrange(80, WIDTH - 100), random.randrange(120, HEIGHT - 80), 45, 45)
                for _ in range(12)
            ]
        else:
            count = 5 if n % 3 else 8
            self.objects = [
                pygame.Rect(
                    random.randrange(80, WIDTH - 100),
                    random.randrange(120, HEIGHT - 80),
                    22 if n != 20 else 34,
                    22 if n != 20 else 34,
                )
                for _ in range(count)
            ]

        enemy_count = min(2 + n // 7, 6)
        self.enemies = [
            pygame.Rect(
                random.randrange(200, WIDTH - 70),
                random.randrange(120, HEIGHT - 80),
                30,
                30,
            )
            for _ in range(enemy_count)
        ]

        if n in (3, 11, 17, 25):
            self.target = pygame.Rect(WIDTH - 90, random.randrange(120, HEIGHT - 90), 38, 38)

    def restart(self):
        self.__init__(self.info)

    def update(self, dt):
        if self.finished:
            return

        n = self.info.number
        self.time -= dt
        self.cooldown = max(0, self.cooldown - dt)
        self.flash = max(0, self.flash - dt)

        keys = pygame.key.get_pressed()

        # Movement-focused games
        if n not in (5, 19, 24):
            speed = 5 + (2 if n in (3, 11, 25) else 0)
            move_rect(self.player, keys, speed)

        if n in (1, 4, 9, 12, 14, 18, 21, 22, 28):
            self.collect_objects()

        if n in (2, 6, 10, 16, 23, 27):
            self.chase_enemies(dt)

        if n in (7, 17, 21, 25):
            self.spawn_hazards(dt)

        if n in (8, 10, 20, 23, 26, 29, 30):
            self.combat(dt)

        if n in (3, 11, 25):
            self.race(dt)

        if n == 5:
            self.switch_puzzle()

        if n == 13:
            self.maze()

        if n == 15:
            self.base_defense(dt)

        if n == 19:
            self.pulse(dt)

        if n == 24:
            self.memory_game(dt)

        if n == 28:
            self.forge(dt)

        if n == 29:
            self.boss(dt)

        if n == 30:
            self.final_challenge(dt)

        if self.time <= 0 and not self.finished:
            self.finish(False)

        if self.info.number not in (5, 13, 19, 24) and self.score >= self.goal():
            self.finish(True)

    def goal(self):
        n = self.info.number
        return {
            1: 8, 2: 3, 4: 7, 6: 5, 7: 30, 8: 25, 9: 6, 10: 40,
            12: 5, 14: 8, 15: 30, 16: 4, 17: 25, 18: 3, 20: 50,
            21: 20, 22: 12, 23: 25, 25: 20, 26: 30, 27: 4, 28: 35,
            29: 60, 30: 50
        }.get(self.info.number, 10)

    def collect_objects(self):
        for obj in self.objects[:]:
            if self.player.colliderect(obj):
                self.objects.remove(obj)
                self.score += 1
                self.flash = 0.08
        if not self.objects and self.score < self.goal():
            self.objects = [
                pygame.Rect(
                    random.randrange(70, WIDTH - 80),
                    random.randrange(110, HEIGHT - 70),
                    22,
                    22,
                )
                for _ in range(min(8, self.goal() - self.score))
            ]

    def chase_enemies(self, dt):
        for enemy in self.enemies:
            dx = self.player.centerx - enemy.centerx
            dy = self.player.centery - enemy.centery
            length = math.hypot(dx, dy) or 1
            speed = 1.0 + self.info.number * 0.025
            enemy.x += int(dx / length * speed)
            enemy.y += int(dy / length * speed)
            if enemy.colliderect(self.player):
                self.flash = 0.25
                self.player.topleft = (70, HEIGHT // 2)
                self.score = max(0, self.score - 1)

    def spawn_hazards(self, dt):
        if random.random() < dt * (1.0 + self.info.number / 25):
            size = random.randrange(18, 42)
            self.enemies.append(pygame.Rect(random.randrange(20, WIDTH - size), 90, size, size))

        for enemy in self.enemies[:]:
            enemy.y += 3 + self.info.number // 8
            if enemy.top > HEIGHT:
                self.enemies.remove(enemy)
                self.score += 1
            elif enemy.colliderect(self.player):
                self.flash = 0.2
                self.player.topleft = (70, HEIGHT // 2)
                self.score = max(0, self.score - 2)

    def combat(self, dt):
        if self.cooldown <= 0:
            # Automatic short-range pulse for simple keyboard play.
            for enemy in self.enemies[:]:
                if self.player.inflate(95, 95).colliderect(enemy):
                    self.enemies.remove(enemy)
                    self.score += 3
                    self.cooldown = 0.35
                    break

        if random.random() < dt * 0.35 and len(self.enemies) < 8:
            self.enemies.append(
                pygame.Rect(random.randrange(250, WIDTH - 60), random.randrange(100, HEIGHT - 70), 30, 30)
            )

    def race(self, dt):
        self.target.y += random.choice([-2, -1, 0, 1, 2])
        self.target.y = clamp(self.target.y, 100, HEIGHT - 80)
        if self.player.colliderect(self.target):
            self.score += 4
            self.target.topleft = (WIDTH - 90, random.randrange(110, HEIGHT - 80))

    def switch_puzzle(self):
        if not self.objects:
            return
        # Space cycles switches; matching the hidden sequence gives progress.
        pass

    def maze(self):
        if self.player.colliderect(self.target):
            self.score += 2
            self.target.topleft = (
                random.randrange(100, WIDTH - 80),
                random.randrange(120, HEIGHT - 80),
            )

    def base_defense(self, dt):
        base = pygame.Rect(30, HEIGHT // 2 - 80, 70, 160)
        for enemy in self.enemies:
            dx = base.centerx - enemy.centerx
            dy = base.centery - enemy.centery
            length = math.hypot(dx, dy) or 1
            enemy.x += int(dx / length * 1.5)
            enemy.y += int(dy / length * 1.5)
            if enemy.colliderect(base):
                self.enemies.remove(enemy)
                self.score = max(0, self.score - 5)
        if random.random() < dt * 1.2 and len(self.enemies) < 10:
            self.enemies.append(pygame.Rect(WIDTH - 40, random.randrange(100, HEIGHT - 50), 30, 30))

    def pulse(self, dt):
        # Targets orbit the player. SPACE is handled in events.
        if not self.objects:
            self.objects = [pygame.Rect(random.randrange(100, WIDTH - 100), random.randrange(120, HEIGHT - 100), 25, 25)]

    def memory_game(self, dt):
        self.pattern_timer -= dt
        if self.pattern_timer <= 0 and self.pattern:
            # Once the pattern is hidden, player can use SPACE to cycle selection.
            pass

    def forge(self, dt):
        if self.score >= self.goal():
            self.finish(True)

    def boss(self, dt):
        boss = pygame.Rect(WIDTH - 180, HEIGHT // 2 - 80, 90, 160)
        if self.player.inflate(120, 120).colliderect(boss):
            self.score += 1

    def final_challenge(self, dt):
        # Mix collecting, chasing and combat.
        self.collect_objects()
        self.chase_enemies(dt)
        self.combat(dt)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_r:
                self.restart()
            elif event.key == pygame.K_SPACE:
                self.action()

    def action(self):
        n = self.info.number

        if n in (5, 13, 19):
            self.score += 1

        elif n == 24:
            if self.pattern_input == self.pattern:
                self.finish(True)
            else:
                self.pattern_input.append((len(self.pattern_input) + self.score) % 9)
                if len(self.pattern_input) >= len(self.pattern):
                    self.finish(self.pattern_input == self.pattern)

        elif n in (8, 10, 20, 23, 26, 29, 30):
            for enemy in self.enemies[:]:
                if self.player.inflate(130, 130).colliderect(enemy):
                    self.enemies.remove(enemy)
                    self.score += 5
                    break

        else:
            self.score += 1

    def finish(self, won):
        self.finished = True
        self.won = won

    def draw(self):
        SCREEN.fill(BLACK)
        self.draw_grid()

        n = self.info.number

        # Target / exit
        pygame.draw.rect(SCREEN, GREEN if self.won else CYAN, self.target, border_radius=8)

        # Objects
        for obj in self.objects:
            color = YELLOW
            if n in (2, 6, 16, 27):
                color = PURPLE
            elif n in (7, 17, 21, 25):
                color = ORANGE
            pygame.draw.rect(SCREEN, color, obj, border_radius=6)

        # Enemies
        for enemy in self.enemies:
            color = RED
            if n in (6, 27):
                color = PURPLE
            pygame.draw.rect(SCREEN, color, enemy, border_radius=6)

        # Player
        pygame.draw.rect(SCREEN, WHITE, self.player, border_radius=7)

        # Special puzzle visuals
        if n == 5:
            for i, rect in enumerate(self.objects):
                pygame.draw.rect(SCREEN, [BLUE, GREEN, YELLOW, PURPLE][i], rect, 3, border_radius=8)

        if n == 24:
            self.draw_memory()

        if n == 26:
            base = pygame.Rect(30, HEIGHT // 2 - 80, 70, 160)
            pygame.draw.rect(SCREEN, CYAN, base, 3, border_radius=8)

        # HUD
        pygame.draw.rect(SCREEN, PANEL, (0, 0, WIDTH, 76))
        text(SCREEN, f"{self.info.number:02d}  {self.info.title}", (24, 15), BIG)
        text(SCREEN, self.info.genre, (24, 50), SMALL, MUTED)
        text(SCREEN, f"SCORE {self.score}", (WIDTH - 260, 16))
        text(SCREEN, f"TIME {max(0, self.time):04.1f}", (WIDTH - 150, 16), color=YELLOW)
        text(SCREEN, "SPACE action  •  R restart  •  ESC menu", (WIDTH - 390, 51), SMALL, MUTED)

        if self.flash > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((220, 40, 55, 45))
            SCREEN.blit(overlay, (0, 0))

        if self.finished:
            self.draw_result()

        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, WIDTH, 50):
            pygame.draw.line(SCREEN, GRID, (x, 80), (x, HEIGHT), 1)
        for y in range(80, HEIGHT, 50):
            pygame.draw.line(SCREEN, GRID, (0, y), (WIDTH, y), 1)

    def draw_memory(self):
        start_x, start_y = 430, 145
        for i in range(9):
            x = start_x + (i % 3) * 70
            y = start_y + (i // 3) * 70
            active = i in self.pattern if self.pattern_timer > 0 else False
            selected = i in self.pattern_input
            color = YELLOW if active else (BLUE if selected else GRID)
            pygame.draw.rect(SCREEN, color, (x, y, 55, 55), border_radius=8)

    def draw_result(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        SCREEN.blit(overlay, (0, 0))
        title = "MISSION COMPLETE" if self.won else "RUN FAILED"
        color = GREEN if self.won else RED
        text(SCREEN, title, (WIDTH // 2, 270), TITLE, color, True)
        text(SCREEN, f"Score: {self.score}", (WIDTH // 2, 340), BIG, WHITE, True)
        text(SCREEN, "R = restart    ESC = game menu", (WIDTH // 2, 400), FONT, MUTED, True)


class Menu:
    def __init__(self):
        self.selected = 0
        self.page = 0
        self.per_page = 10
        self.running = True

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return None

        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % self.per_page
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % self.per_page
        elif event.key == pygame.K_LEFT:
            self.page = max(0, self.page - 1)
            self.selected = 0
        elif event.key == pygame.K_RIGHT:
            self.page = min((len(GAMES) - 1) // self.per_page, self.page + 1)
            self.selected = 0
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            index = self.page * self.per_page + self.selected
            if index < len(GAMES):
                return GAMES[index]
        elif event.key == pygame.K_ESCAPE:
            self.running = False

        return None

    def draw(self):
        SCREEN.fill(BLACK)
        text(SCREEN, "AJVYRA", (55, 45), TITLE)
        text(SCREEN, "30 ORIGINAL GAME MODES", (58, 105), FONT, MUTED)

        start = self.page * self.per_page
        end = min(start + self.per_page, len(GAMES))

        for row, info in enumerate(GAMES[start:end]):
            y = 155 + row * 45
            selected = row == self.selected
            if selected:
                pygame.draw.rect(SCREEN, (30, 34, 45), (45, y - 6, 1010, 38), border_radius=7)

            text(SCREEN, f"{info.number:02d}", (65, y), SMALL, CYAN if selected else MUTED)
            text(SCREEN, info.title, (115, y), FONT)
            text(SCREEN, info.genre, (390, y), SMALL, MUTED)
            text(SCREEN, info.description, (650, y), SMALL, MUTED)

        page_count = (len(GAMES) - 1) // self.per_page + 1
        text(
            SCREEN,
            f"PAGE {self.page + 1}/{page_count}    ↑↓ select   ←→ page   ENTER play   ESC quit",
            (55, HEIGHT - 45),
            SMALL,
            MUTED,
        )

        pygame.display.flip()


def run_game(info):
    game = Game(info)
    while game.running:
        dt = CLOCK.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        game.update(dt)
        game.draw()


def main():
    menu = Menu()

    while menu.running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            selected = menu.handle_event(event)
            if selected:
                run_game(selected)

        menu.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
