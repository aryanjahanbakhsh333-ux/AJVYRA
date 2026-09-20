import pygame


class Checkpoint:

    def __init__(self, x, y):
        self.position = (x, y)

        self.rect = pygame.Rect(
            x,
            y,
            35,
            80
        )

        self.active = False

    def activate(self):
        self.active = True

    def draw(self, screen, camera_x):

        x = self.rect.x - camera_x

        color = (
            (245, 245, 245)
            if self.active
            else (70, 70, 70)
        )

        pygame.draw.rect(
            screen,
            color,
            (
                x,
                self.rect.y,
                self.rect.width,
                self.rect.height
            )
        )
