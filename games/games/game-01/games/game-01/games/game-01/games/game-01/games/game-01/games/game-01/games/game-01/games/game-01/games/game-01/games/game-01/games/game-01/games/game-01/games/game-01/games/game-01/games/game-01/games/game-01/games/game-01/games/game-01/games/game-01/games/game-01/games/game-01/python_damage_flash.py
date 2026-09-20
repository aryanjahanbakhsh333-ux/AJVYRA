import pygame


class DamageFlash:

    def __init__(self):

        self.timer = 0
        self.duration = 10

    def trigger(self):

        self.timer = self.duration

    def update(self):

        if self.timer > 0:
            self.timer -= 1

    def draw(self, screen):

        if self.timer <= 0:
            return

        alpha = int(
            90 *
            (self.timer / self.duration)
        )

        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill(
            (255, 255, 255, alpha)
        )

        screen.blit(
            overlay,
            (0, 0)
        )
