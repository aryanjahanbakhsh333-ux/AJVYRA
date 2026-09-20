import pygame


class PythonPlayer:

    def __init__(self, x, y, config):

        self.rect = pygame.Rect(
            x,
            y,
            config.PLAYER_WIDTH,
            config.PLAYER_HEIGHT
        )

        self.velocity_y = 0

        self.speed = config.PLAYER_SPEED

        self.jump_power = config.JUMP_POWER

        self.gravity = config.GRAVITY

        self.health = config.MAX_HEALTH

        self.facing = 1

        self.on_ground = False

        self.invulnerable_timer = 0

    def move(self, keys):

        velocity_x = 0

        if (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
        ):

            velocity_x = -self.speed

            self.facing = -1

        if (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        ):

            velocity_x = self.speed

            self.facing = 1

        self.rect.x += velocity_x

    def jump(self):

        if self.on_ground:

            self.velocity_y = self.jump_power

            self.on_ground = False

    def physics(self, platforms):

        self.velocity_y += self.gravity

        self.rect.y += int(
            self.velocity_y
        )

        self.on_ground = False

        for platform in platforms:

            if self.rect.colliderect(platform):

                if self.velocity_y > 0:

                    self.rect.bottom = platform.top

                    self.velocity_y = 0

                    self.on_ground = True

    def damage(self, amount):

        if self.invulnerable_timer > 0:

            return False

        self.health -= amount

        self.invulnerable_timer = 45

        return self.health <= 0

    def update_timer(self):

        if self.invulnerable_timer > 0:

            self.invulnerable_timer -= 1

    def draw(self, screen, colors):

        pygame.draw.rect(
            screen,
            colors.WHITE,
            self.rect
        )

        eye_x = (
            self.rect.right - 10
            if self.facing == 1
            else self.rect.left + 6
        )

        pygame.draw.rect(
            screen,
            colors.BLACK,
            (
                eye_x,
                self.rect.y + 12,
                4,
                4
            )
        )
