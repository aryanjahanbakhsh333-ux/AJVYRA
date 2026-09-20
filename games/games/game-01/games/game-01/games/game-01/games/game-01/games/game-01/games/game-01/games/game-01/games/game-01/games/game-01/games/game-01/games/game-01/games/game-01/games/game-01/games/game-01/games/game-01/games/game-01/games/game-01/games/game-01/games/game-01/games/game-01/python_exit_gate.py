import pygame


class ExitGate:

    def __init__(self, x, y):

        self.rect = pygame.Rect(
            x,
            y,
            45,
            120
        )

        self.unlocked = False

    def unlock(self):

        self.unlocked = True

    def can_exit(self, player):

        return (
            self.unlocked
            and
            self.rect.colliderect(player)
        )

    def draw(self, screen, camera_x):

        rect = self.rect.move(
            -int(camera_x),
            0
        )

        color = (
            (245, 245, 245)
            if self.unlocked
            else (55, 55, 55)
        )

        pygame.draw.rect(
            screen,
            color,
            rect
        )

        pygame.draw.rect(
            screen,
            (10, 10, 10),
            (
                rect.x + 10,
                rect.y + 10,
                rect.width - 20,
                rect.height - 20
            )
        )
