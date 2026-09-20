import pygame
import sys
import random

pygame.init()

# -----------------------------
# SETTINGS
# -----------------------------

WIDTH = 1100
HEIGHT = 650
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AJVYRA — Black Run")

clock = pygame.time.Clock()

# -----------------------------
# COLORS
# -----------------------------

BLACK = (5, 5, 5)
DARK = (15, 15, 15)
GRAY = (45, 45, 45)
LIGHT_GRAY = (120, 120, 120)
WHITE = (245, 245, 245)

# -----------------------------
# FONT
# -----------------------------

font_big = pygame.font.SysFont("arial", 54, bold=True)
font = pygame.font.SysFont("arial", 22)
font_small = pygame.font.SysFont("arial", 15)

# -----------------------------
# PLAYER
# -----------------------------

player = pygame.Rect(100, 500, 35, 50)

player_velocity_x = 0
player_velocity_y = 0

PLAYER_SPEED = 6
JUMP_POWER = -17
GRAVITY = 0.8

on_ground = False
facing = 1

health = 100
score = 0

# -----------------------------
# PLATFORMS
# -----------------------------

platforms = [
    pygame.Rect(0, 590, 500, 60),
    pygame.Rect(580, 510, 260, 35),
    pygame.Rect(900, 430, 250, 35),
    pygame.Rect(1100, 590, 400, 60),
]

# -----------------------------
# ORBS
# -----------------------------

orbs = [
    pygame.Rect(250, 550, 18, 18),
    pygame.Rect(650, 470, 18, 18),
    pygame.Rect(950, 390, 18, 18),
]

# -----------------------------
# ENEMIES
# -----------------------------

enemies = [
    {
        "rect": pygame.Rect(420, 540, 35, 45),
        "health": 30,
        "direction": -1
    },
    {
        "rect": pygame.Rect(700, 465, 35, 45),
        "health": 30,
        "direction": 1
    },
    {
        "rect": pygame.Rect(1000, 385, 35, 45),
        "health": 30,
        "direction": -1
    }
]

# -----------------------------
# PARTICLES
# -----------------------------

particles = []


def create_particles(x, y):

    for _ in range(12):

        particles.append({
            "x": x,
            "y": y,
            "vx": random.uniform(-4, 4),
            "vy": random.uniform(-4, 1),
            "life": random.randint(15, 30)
        })


def update_particles():

    for particle in particles[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["vy"] += 0.15

        particle["life"] -= 1

        if particle["life"] <= 0:
            particles.remove(particle)


def draw_particles():

    for particle in particles:

        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            3
        )


# -----------------------------
# DRAW BACKGROUND
# -----------------------------

def draw_background():

    screen.fill(BLACK)

    # Moon
    pygame.draw.circle(
        screen,
        (25, 25, 25),
        (900, 120),
        80
    )

    # Stars
    random.seed(10)

    for _ in range(80):

        x = random.randint(0, WIDTH)
        y = random.randint(0, 400)

        pygame.draw.circle(
            screen,
            (50, 50, 50),
            (x, y),
            1
        )


# -----------------------------
# DRAW PLAYER
# -----------------------------

def draw_player():

    pygame.draw.rect(
        screen,
        WHITE,
        player
    )

    # Eye / direction indicator

    eye_x = (
        player.right - 9
        if facing == 1
        else player.left + 5
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (
            eye_x,
            player.y + 10,
            4,
            4
        )
    )


# -----------------------------
# DRAW PLATFORMS
# -----------------------------

def draw_platforms():

    for platform in platforms:

        pygame.draw.rect(
            screen,
            DARK,
            platform
        )

        pygame.draw.rect(
            screen,
            GRAY,
            (
                platform.x,
                platform.y,
                platform.width,
                4
            )
        )


# -----------------------------
# DRAW ORBS
# -----------------------------

def draw_orbs():

    for orb in orbs:

        center = orb.center

        pygame.draw.circle(
            screen,
            WHITE,
            center,
            10
        )

        pygame.draw.circle(
            screen,
            GRAY,
            center,
            16,
            2
        )


# -----------------------------
# DRAW ENEMIES
# -----------------------------

def draw_enemies():

    for enemy in enemies:

        rect = enemy["rect"]

        pygame.draw.rect(
            screen,
            LIGHT_GRAY,
            rect
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (
                rect.x + 8,
                rect.y + 10,
                5,
                5
            )
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (
                rect.x + 22,
                rect.y + 10,
                5,
                5
            )
        )


# -----------------------------
# HUD
# -----------------------------

def draw_hud():

    score_text = font.render(
        f"SCORE {score:06d}",
        True,
        WHITE
    )

    health_text = font.render(
        f"HP {health}",
        True,
        WHITE
    )

    orb_text = font.render(
        f"ORBS {3 - len(orbs)} / 3",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (25, 20)
    )

    screen.blit(
        health_text,
        (25, 50)
    )

    screen.blit(
        orb_text,
        (25, 80)
    )


# -----------------------------
# ATTACK
# -----------------------------

def attack():

    global score

    attack_range = pygame.Rect(
        player.right
        if facing == 1
        else player.left - 60,
        player.y + 10,
        60,
        30
    )

    for enemy in enemies[:]:

        if attack_range.colliderect(
            enemy["rect"]
        ):

            enemy["health"] -= 20

            create_particles(
                enemy["rect"].centerx,
                enemy["rect"].centery
            )

            if enemy["health"] <= 0:

                enemies.remove(enemy)

                score += 100


# -----------------------------
# ENEMY AI
# -----------------------------

def update_enemies():

    global health

    for enemy in enemies:

        rect = enemy["rect"]

        distance = player.centerx - rect.centerx

        if abs(distance) < 300:

            if distance > 0:
                rect.x += 2

            else:
                rect.x -= 2

        else:

            rect.x += enemy["direction"] * 2

        # Enemy collision

        if player.colliderect(rect):

            health -= 1

            if health <= 0:

                game_over()


# -----------------------------
# GAME OVER
# -----------------------------

def game_over():

    screen.fill(BLACK)

    title = font_big.render(
        "RUN OVER",
        True,
        WHITE
    )

    score_text = font.render(
        f"SCORE {score}",
        True,
        LIGHT_GRAY
    )

    restart = font_small.render(
        "PRESS ENTER TO RESTART",
        True,
        LIGHT_GRAY
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            240
        )
    )

    screen.blit(
        score_text,
        (
            WIDTH // 2 - score_text.get_width() // 2,
            320
        )
    )

    screen.blit(
        restart,
        (
            WIDTH // 2 - restart.get_width() // 2,
            370
        )
    )

    pygame.display.flip()

    waiting = True

    while waiting:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_RETURN
            ):
                restart_game()
                waiting = False

        clock.tick(FPS)


# -----------------------------
# RESTART
# -----------------------------

def restart_game():

    global player
    global health
    global score
    global orbs
    global enemies

    player.x = 100
    player.y = 500

    health = 100
    score = 0

    orbs = [
        pygame.Rect(250, 550, 18, 18),
        pygame.Rect(650, 470, 18, 18),
        pygame.Rect(950, 390, 18, 18)
    ]

    enemies = [
        {
            "rect": pygame.Rect(420, 540, 35, 45),
            "health": 30,
            "direction": -1
        },
        {
            "rect": pygame.Rect(700, 465, 35, 45),
            "health": 30,
            "direction": 1
        },
        {
            "rect": pygame.Rect(1000, 385, 35, 45),
            "health": 30,
            "direction": -1
        }
    ]


# -----------------------------
# MAIN LOOP
# -----------------------------

running = True

while running:

    clock.tick(FPS)

    # EVENTS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if on_ground:
                    player_velocity_y = JUMP_POWER

            if event.key == pygame.K_f:
                attack()

    # -------------------------
    # INPUT
    # -------------------------

    keys = pygame.key.get_pressed()

    player_velocity_x = 0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:

        player_velocity_x = -PLAYER_SPEED
        facing = -1

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:

        player_velocity_x = PLAYER_SPEED
        facing = 1

    # -------------------------
    # HORIZONTAL MOVEMENT
    # -------------------------

    player.x += player_velocity_x

    # -------------------------
    # GRAVITY
    # -------------------------

    player_velocity_y += GRAVITY

    player.y += player_velocity_y

    on_ground = False

    # -------------------------
    # PLATFORM COLLISION
    # -------------------------

    for platform in platforms:

        if player.colliderect(platform):

            if player_velocity_y > 0:

                player.bottom = platform.top

                player_velocity_y = 0

                on_ground = True

    # -------------------------
    # ORB COLLECTION
    # -------------------------

    for orb in orbs[:]:

        if player.colliderect(orb):

            orbs.remove(orb)

            score += 250

            create_particles(
                orb.centerx,
                orb.centery
            )

    # -------------------------
    # ENEMIES
    # -------------------------

    update_enemies()

    # -------------------------
    # FALLING
    # -------------------------

    if player.y > HEIGHT:

        health = 0
        game_over()

    # -------------------------
    # PARTICLES
    # -------------------------

    update_particles()

    # -------------------------
    # DRAW
    # -------------------------

    draw_background()

    draw_platforms()

    draw_orbs()

    draw_enemies()

    draw_particles()

    draw_player()

    draw_hud()

    # -------------------------
    # WIN CONDITION
    # -------------------------

    if len(orbs) == 0:

        win_text = font_big.render(
            "EXIT UNLOCKED",
            True,
            WHITE
        )

        screen.blit(
            win_text,
            (
                WIDTH // 2 -
                win_text.get_width() // 2,
                120
            )
        )

    pygame.display.flip()


pygame.quit()
sys.exit()
