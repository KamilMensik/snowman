import pygame
from pygame.locals import *
from pygame.math import Vector2
import bullets
import math
import os

sprites = {}
small_enemies = pygame.sprite.Group()

for i in os.listdir('sprites/small_enemies'):
    sprites[i] = []
    for j in os.listdir(f'sprites/small_enemies/{i}'):
        sprites[i].append(pygame.image.load(f'sprites/small_enemies/{i}/{j}').convert_alpha())

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, data_file, angle) -> None:
        pygame.sprite.Sprite.__init__(self)
        data = eval('\t'.join([line.strip() for line in open(data_file).readlines()]))
        self.hp = data.get('hp')
        self.velocity = Vector2(0.1 * data.get('speed'), 0).rotate(angle) * 5
        self.attacks = data.get('attacks')
        self.name = data.get('name')
        self.image = sprites[self.name][0]
        self.rect = self.image.get_rect().move(300, 300)
        self.position = Vector2(self.rect.center)
        self.animation_frame = 0
        small_enemies.add(self)

    def update(self, should_animate) -> None:
        self.position += self.velocity
        self.rect.center = self.position
        if should_animate: self.animate()

    def check_hitbox(self):
        return

    def animate(self):
        self.animation_frame += 1
        if self.animation_frame >= len(sprites[self.name]):
            self.animation_frame = 0
        frame = self.animation_frame
        self.image = sprites[self.name][frame]