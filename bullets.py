import sys, pygame
from pygame.locals import *
from pygame.math import Vector2

bullets = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, speed, position, radius = 8, type = 'enemy') -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.velocity = Vector2(0.1 * speed, 0).rotate(angle) * 5
        self.pos = Vector2(self.rect.center)
        self.radius = radius
        if type == 'enemy':
            bullets.add(self)
        elif type == 'player':
            player_bullets.add(self)
    
    def update(self) -> None:
        self.pos += self.velocity
        self.rect.center = self.pos
        if self.pos.x <= -50 or self.pos.x >= 850 or self.pos.y <= -50 or self.pos.y >= 850:
            self.kill()