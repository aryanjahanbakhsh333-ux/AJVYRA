import pygame


class CombatSystem:

    def __init__(self, player):

        self.player = player

        self.damage = 20

        self.range = 75

        self.cooldown = 0

    def update(self):

        if self.cooldown > 0:

            self.cooldown -= 1

    def attack(self):

        if self.cooldown > 0:

            return None

        self.cooldown = 18

        if self.player.facing == 1:

            return pygame.Rect(
                self.player.rect.right,
                self.player.rect.y + 8,
                self.range,
                35
            )

        return pygame.Rect(
            self.player.rect.left - self.range,
            self.player.rect.y + 8,
            self.range,
            35
        )
