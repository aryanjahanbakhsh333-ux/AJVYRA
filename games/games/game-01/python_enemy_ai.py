import pygame


class EnemyAI:

    def __init__(self, rect):

        self.rect = rect

        self.health = 30

        self.speed = 2

        self.direction = 1

        self.detection_range = 330

        self.attack_distance = 35

    def update(self, player):

        distance = (
            player.centerx -
            self.rect.centerx
        )

        if abs(distance) <= self.detection_range:

            if distance > 0:
                self.rect.x += self.speed
                self.direction = 1

            elif distance < 0:
                self.rect.x -= self.speed
                self.direction = -1

        else:

            self.rect.x += (
                self.speed *
                self.direction
            )

    def take_damage(self, amount):

        self.health -= amount

        return self.health <= 0

    def touching_player(self, player):

        return self.rect.colliderect(player)
