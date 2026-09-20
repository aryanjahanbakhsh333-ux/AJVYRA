import pygame


class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        self.title_font = pygame.font.SysFont(
            "arial",
            64,
            bold=True
        )

        self.info_font = pygame.font.SysFont(
            "arial",
            18
        )

    def show(self):
        waiting = True

        while waiting:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.KEYDOWN:

                    if event.key in (
                        pygame.K_RETURN,
                        pygame.K_SPACE
                    ):
                        waiting = False

            self.screen.fill((5, 5, 5))

            title = self.title_font.render(
                "BLACK RUN",
                True,
                (245, 245, 245)
            )

            subtitle = self.info_font.render(
                "AJVYRA // GAME 01",
                True,
                (110, 110, 110)
            )

            start = self.info_font.render(
                "PRESS ENTER TO START",
                True,
                (180, 180, 180)
            )

            self.screen.blit(
                title,
                (
                    self.screen.get_width() // 2 -
                    title.get_width() // 2,
                    220
                )
            )

            self.screen.blit(
                subtitle,
                (
                    self.screen.get_width() // 2 -
                    subtitle.get_width() // 2,
                    300
                )
            )

            self.screen.blit(
                start,
                (
                    self.screen.get_width() // 2 -
                    start.get_width() // 2,
                    370
                )
            )

            pygame.display.flip()
