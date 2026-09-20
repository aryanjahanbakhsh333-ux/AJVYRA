import random


class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.vx = random.uniform(
            -4,
            4
        )

        self.vy = random.uniform(
            -5,
            1
        )

        self.life = random.randint(
            15,
            35
        )

    def update(self):

        self.x += self.vx

        self.y += self.vy

        self.vy += 0.15

        self.life -= 1

    def alive(self):

        return self.life > 0


class ParticleSystem:

    def __init__(self):

        self.particles = []

    def burst(
        self,
        x,
        y,
        amount=12
    ):

        for _ in range(amount):

            self.particles.append(
                Particle(x, y)
            )

    def update(self):

        for particle in self.particles[:]:

            particle.update()

            if not particle.alive():

                self.particles.remove(
                    particle
                )

    def draw(self, screen, camera):

        import pygame

        for particle in self.particles:

            pygame.draw.circle(
                screen,
                (245, 245, 245),
                (
                    int(
                        particle.x -
                        camera.x
                    ),
                    int(particle.y)
                ),
                3
            )
