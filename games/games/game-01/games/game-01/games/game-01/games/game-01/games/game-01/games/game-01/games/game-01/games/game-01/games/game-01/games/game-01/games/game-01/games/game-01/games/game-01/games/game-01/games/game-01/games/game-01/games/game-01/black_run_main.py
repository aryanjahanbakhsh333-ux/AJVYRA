import pygame

from python_config import *
import python_colors as colors

from python_player import PythonPlayer
from python_platforms import create_platforms
from python_orbs import OrbManager
from python_enemy_manager import EnemyManager
from python_combat import CombatSystem
from python_camera import Camera
from python_particles import ParticleSystem

from python_hud import HUD
from python_game_state import GameState
from python_menu import MainMenu
from python_pause import PauseScreen
from python_save_system import SaveSystem
from python_sound import SoundSystem
from python_collision import CollisionSystem
from python_results import ResultsScreen


class BlackRun:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "arial",
            22
        )

        self.state = GameState()

        self.player = PythonPlayer(
            100,
            500,
            __import__("python_config")
        )

        self.platforms = create_platforms()

        self.orbs = OrbManager()

        self.enemies = EnemyManager()

        self.combat = CombatSystem(
            self.player
        )

        self.camera = Camera(
            WIDTH,
            WORLD_WIDTH
        )

        self.particles = ParticleSystem()

        self.hud = HUD(
            self.font
        )

        self.menu = MainMenu(
            self.screen
        )

        self.pause_screen = PauseScreen(
            self.screen
        )

        self.save = SaveSystem()

        self.sound = SoundSystem()

        self.results = ResultsScreen(
            self.screen
        )

        self.running = True

        self.attack_requested = False

    def start(self):

        self.menu.show()

        while self.running:

            self.state.reset()

            self.reset_level()

            self.play_level()

            if self.state.completed:

                self.results.show(
                    "RUN COMPLETE",
                    self.state.score,
                    self.state.collected_orbs
                )

            elif self.state.game_over:

                self.results.show(
                    "RUN OVER",
                    self.state.score,
                    self.state.collected_orbs
                )

            else:
                break

        self.sound.shutdown()
        pygame.quit()

    def reset_level(self):

        self.player = PythonPlayer(
            100,
            500,
            __import__("python_config")
        )

        self.orbs.reset()

        self.enemies.reset()

        self.combat = CombatSystem(
            self.player
        )

        self.particles.particles.clear()

    def play_level(self):

        while self.state.running:

            self.handle_events()

            keys = pygame.key.get_pressed()

            self.player.move(keys)

            self.player.physics(
                self.platforms
            )

            self.player.update_timer()

            self.resolve_world()

            self.update_gameplay()

            self.draw()

            self.clock.tick(FPS)

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False
                self.state.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    self.player.jump()

                elif event.key == pygame.K_f:

                    self.attack_requested = True

                elif event.key == pygame.K_ESCAPE:

                    self.pause_screen.show()

    def update_gameplay(self):

        self.enemies.update(
            self.player.rect
        )

        self.combat.update()

        if self.attack_requested:

            attack_rect = self.combat.attack()

            self.attack_requested = False

            if attack_rect:

                defeated = self.enemies.damage_nearby(
                    attack_rect,
                    self.combat.damage
                )

                if defeated:

                    self.state.add_score(
                        defeated * ENEMY_SCORE
                    )

                    self.particles.burst(
                        self.player.rect.centerx,
                        self.player.rect.centery
                    )

                    self.sound.attack()

        damage_hits = self.enemies.player_damage(
            self.player.rect
        )

        if damage_hits:

            dead = self.player.damage(
                damage_hits
            )

            if dead:

                self.state.health = 0
                self.state.game_over = True
                self.state.running = False

                self.sound.game_over()

        self.collect_orbs()

        self.particles.update()

        self.camera.update(
            self.player.rect
        )

        self.state.health = self.player.health

        if self.orbs.completed():

            if self.player.rect.x > 3200:

                self.state.finish()

                self.sound.victory()

    def collect_orbs(self):

        collected = self.orbs.collect(
            self.player.rect
        )

        if collected:

            for _ in range(collected):

                self.state.collect_orb()

                self.sound.collect()

                self.particles.burst(
                    self.player.rect.centerx,
                    self.player.rect.centery
                )

    def resolve_world(self):

        self.player.rect.x = max(
            0,
            min(
                self.player.rect.x,
                WORLD_WIDTH -
                self.player.rect.width
            )
        )

        if self.player.rect.y > WORLD_HEIGHT:

            self.state.game_over = True
            self.state.running = False

            self.sound.game_over()

    def draw(self):

        self.draw_background()

        self.draw_world()

        self.hud.draw(
            self.screen,
            self.state.score,
            self.state.health,
            self.state.collected_orbs,
            8
        )

        self.hud.draw_controls(
            self.screen
        )

        pygame.display.flip()

    def draw_background(self):

        self.screen.fill(
            colors.BLACK
        )

        for i in range(70):

            x = (
                i * 137 -
                int(self.camera.x * 0.15)
            ) % WORLD_WIDTH

            y = (
                i * 71
            ) % 420

            if 0 <= x <= WIDTH:

                pygame.draw.circle(
                    self.screen,
                    colors.GRAY,
                    (int(x), int(y)),
                    1
                )

    def draw_world(self):

        for platform in self.platforms:

            visible = self.camera.apply(
                platform
            )

            if visible.right < 0:
                continue

            if visible.left > WIDTH:
                continue

            pygame.draw.rect(
                self.screen,
                colors.DARK,
                visible
            )

            pygame.draw.rect(
                self.screen,
                colors.GRAY,
                (
                    visible.x,
                    visible.y,
                    visible.width,
                    4
                )
            )

        self.orbs.draw(
            self.screen,
            colors
        )

        self.enemies.draw(
            self.screen,
            colors
        )

        self.particles.draw(
            self.screen,
            self.camera
        )

        player_rect = self.camera.apply(
            self.player.rect
        )

        pygame.draw.rect(
            self.screen,
            colors.WHITE,
            player_rect
        )

        eye_x = (
            player_rect.right - 10
            if self.player.facing == 1
            else player_rect.left + 6
        )

        pygame.draw.rect(
            self.screen,
            colors.BLACK,
            (
                eye_x,
                player_rect.y + 12,
                4,
                4
            )
        )


if __name__ == "__main__":

    game = BlackRun()

    game.start()
