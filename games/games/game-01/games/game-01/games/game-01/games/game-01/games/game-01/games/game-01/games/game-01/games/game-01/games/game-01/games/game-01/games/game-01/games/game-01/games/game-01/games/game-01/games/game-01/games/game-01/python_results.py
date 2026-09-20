import pygame


class ResultsScreen:

    def __init__(self, screen):

        self.screen = screen

        self.title_font = pygame.font.SysFont(
            "arial",
            52,
            bold=True
        )

        self.font = pygame.font.SysFont(
            "arial",
            22
        )

    def show(
        self,
        title,
        score,
        orbs
    ):

        waiting = True

        while waiting:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.KEYDOWN:

                    if event.key in (
                        pygame.K_RETURN,
                        pygame.K_ESCAPE
                    ):
                        waiting = False

            self.screen.fill(
                (5, 5, 5)
            )

            title_surface = (
                self.title_font.render(
                    title,
                    True,
                    (245, 245, 245)
                )
            )

            score_surface = (
                self.font.render(
                    f"SCORE  {score}",
                    True,
                    (190, 190, 190)
                )
            )

            orb_surface = (
                self.font.render(
                    f"ORBS  {orbs}",
                    True,
                    (150, 150, 150)
                )
            )

            continue_surface = (
                self.font.render(
                    "PRESS ENTER",
                    True,
                    (100, 100, 100)
                )
            )

            center = (
                self.screen.get_width() // 2
            )

            self.screen.blit(
                title_surface,
                (
                    center -
                    title_surface.get_width() // 2,
                    190
                )
            )

            self.screen.blit(
                score_surface,
                (
                    center -
                    score_surface.get_width() // 2,
                    290
                )
            )

            self.screen.blit(
                orb_surface,
                (
                    center -
                    orb_surface.get_width() // 2,
                    330
                )
            )

            self.screen.blit(
                continue_surface,
                (
                    center -
                    continue_surface.get_width() // 2,
                    420
                )
            )

            pygame.display.flip()
