import pygame


class OrbManager:

    def __init__(self):
        self.orbs = []

        self.positions = [
            (250, 550),
            (720, 480),
            (1080, 400),
            (1450, 520),
            (1900, 430),
            (2320, 540),
            (2820, 460),
            (3300, 550),
        ]

        self.reset()

    def reset(self):

        self.orbs = [
            pygame.Rect(
                x,
                y,
                18,
                18
            )
            for x, y in self.positions
        ]

    def collect(self, player):

        collected = 0

        for orb in self.orbs[:]:

            if player.colliderect(orb):

                self.orbs.remove(orb)

                collected += 1

        return collected

    def completed(self):

        return len(self.orbs) == 0

    def draw(self, screen, colors):

        for orb in self.orbs:

            pygame.draw.circle(
                screen,
                colors.WHITE,
                orb.center,
                10
            )

            pygame.draw.circle(
                screen,
                colors.GRAY,
                orb.center,
                16,
                2
            )
