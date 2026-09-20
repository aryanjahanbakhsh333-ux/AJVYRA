import pygame


class PauseScreen:

    def __init__(self, screen):
        self.screen = screen

        self.font = pygame.font.SysFont(
            "arial",
            48,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            "arial",
            18
        )

    def show(self):

        paused = True

        while paused:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        paused = False

            overlay = pygame.Surface(
                self.screen.get_size(),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 190)
            )

            self.screen.blit(
                overlay,
                (0, 0)
            )

            title = self.font.render(
                "PAUSED",
                True,
                (245, 245, 245)
            )

            info = self.small_font.render(
                "PRESS ESC TO CONTINUE",
                True,
                (140, 140, 140)
            )

            self.screen.blit(
                title,
                (
                    self.screen.get_width() // 2 -
                    title.get_width() // 2,
                    250
                )
            )

            self.screen.blit(
                info,
                (
                    self.screen.get_width() // 2 -
                    info.get_width() // 2,
                    320
                )
            )

            pygame.display.flip()
