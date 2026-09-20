import pygame


class SoundSystem:

    def __init__(self):
        self.enabled = True

        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False

    def play_beep(
        self,
        frequency=500,
        duration=80
    ):
        """
        Placeholder sound hook.

        Real WAV/OGG assets can be connected later.
        """

        if not self.enabled:
            return

    def collect(self):
        self.play_beep(800, 80)

    def attack(self):
        self.play_beep(350, 60)

    def damage(self):
        self.play_beep(120, 100)

    def victory(self):
        self.play_beep(900, 180)

    def game_over(self):
        self.play_beep(100, 250)

    def shutdown(self):

        if self.enabled:
            pygame.mixer.quit()
