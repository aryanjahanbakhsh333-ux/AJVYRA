import pygame


def create_platforms():
    return [
        pygame.Rect(0, 590, 520, 60),

        pygame.Rect(620, 520, 260, 35),

        pygame.Rect(970, 440, 260, 35),

        pygame.Rect(1320, 560, 330, 35),

        pygame.Rect(1770, 470, 300, 35),

        pygame.Rect(2190, 580, 360, 35),

        pygame.Rect(2700, 500, 300, 35),

        pygame.Rect(3150, 590, 450, 60),
    ]


def draw_platforms(screen, platforms, colors):
    for platform in platforms:

        pygame.draw.rect(
            screen,
            colors.DARK,
            platform
        )

        pygame.draw.rect(
            screen,
            colors.GRAY,
            (
                platform.x,
                platform.y,
                platform.width,
                4
            )
        )
