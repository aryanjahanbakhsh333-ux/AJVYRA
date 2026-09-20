import pygame


class HUD:
    def __init__(self, font):
        self.font = font
        self.small_font = pygame.font.SysFont("arial", 16)

    def draw(self, screen, score, health, orb_count, total_orbs):
        score_text = self.font.render(
            f"SCORE {score:06d}",
            True,
            (245, 245, 245)
        )

        health_text = self.font.render(
            f"HP {max(0, health)}",
            True,
            (245, 245, 245)
        )

        orb_text = self.font.render(
            f"ORBS {orb_count}/{total_orbs}",
            True,
            (190, 190, 190)
        )

        screen.blit(score_text, (25, 20))
        screen.blit(health_text, (25, 50))
        screen.blit(orb_text, (25, 80))

    def draw_controls(self, screen):
        text = self.small_font.render(
            "A/D or ARROWS  •  SPACE = JUMP  •  F = ATTACK",
            True,
            (100, 100, 100)
        )

        screen.blit(
            text,
            (
                screen.get_width() // 2 - text.get_width() // 2,
                screen.get_height() - 28
            )
        )
