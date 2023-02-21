import pygame
from pygame.math import Vector2
import random

points = pygame.sprite.Group()

class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, image) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=(x,y))
        self.steps = 0
        self.rand_velocity = Vector2(1,0).rotate(random.random()*360)
        points.add(self)

    def check_collision(self, player):
        if pygame.Rect.colliderect(self.rect, player.position):
            player.points += 1
            self.kill()
  
    def update(self, player) -> None:
        if self.rect.x <= -50 or self.rect.x >= 850 or self.rect.y <= -50 or self.rect.y >= 850:
            self.kill()
        if self.steps < 15:
            self.rect.center += (self.rand_velocity * (5 / (self.steps + 1)))
            self.steps += 1
        self.rect.y +=1.5
        self.check_collision(player)