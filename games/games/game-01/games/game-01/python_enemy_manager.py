import pygame
from python_enemy_ai import EnemyAI


class EnemyManager:

    def __init__(self):

        self.enemies = []

        self.spawn_points = [
            (450, 540),
            (760, 465),
            (1140, 385),
            (1550, 505),
            (1980, 415),
            (2460, 525),
            (2910, 445),
        ]

        self.reset()

    def reset(self):

        self.enemies.clear()

        for x, y in self.spawn_points:

            enemy = EnemyAI(
                pygame.Rect(
                    x,
                    y,
                    38,
                    48
                )
            )

            self.enemies.append(enemy)

    def update(self, player):

        for enemy in self.enemies:
            enemy.update(player)

    def damage_nearby(
        self,
        attack_rect,
        damage
    ):

        defeated = 0

        for enemy in self.enemies[:]:

            if attack_rect.colliderect(
                enemy.rect
            ):

                if enemy.take_damage(damage):

                    self.enemies.remove(enemy)

                    defeated += 1

        return defeated

    def player_damage(self, player):

        damage_count = 0

        for enemy in self.enemies:

            if enemy.touching_player(player):

                damage_count += 1

        return damage_count

    def draw(self, screen, colors):

        for enemy in self.enemies:

            pygame.draw.rect(
                screen,
                colors.LIGHT_GRAY,
                enemy.rect
            )

            pygame.draw.rect(
                screen,
                colors.BLACK,
                (
                    enemy.rect.x + 8,
                    enemy.rect.y + 10,
                    5,
                    5
                )
            )

            pygame.draw.rect(
                screen,
                colors.BLACK,
                (
                    enemy.rect.x + 25,
                    enemy.rect.y + 10,
                    5,
                    5
                )
            )
