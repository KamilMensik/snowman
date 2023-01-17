import pygame
from pygame.locals import *
from pygame.math import Vector2
import bullets
import math
import os
import points
small_enemies = pygame.sprite.Group()
sprites = {}
points_sprite = pygame.image.load('sprites/score.png').convert_alpha()

for i in os.listdir('sprites/small_enemies'):
    sprites[i] = []
    for j in os.listdir(f'sprites/small_enemies/{i}'):
        sprites[i].append(pygame.image.load(f'sprites/small_enemies/{i}/{j}').convert_alpha())

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, data_file, position_x, position_y) -> None:
        pygame.sprite.Sprite.__init__(self)
        data = eval('\t'.join([line.strip() for line in open(data_file).readlines()]))
        self.hp = data.get('hp')
        self.velocity = Vector2(0 * data.get('speed'), 0)
        self.attacks = data.get('attacks')
        self.name = data.get('name')
        self.image = sprites[self.name][0]
        self.rect = self.image.get_rect().move(position_x, position_y)
        self.position = Vector2(self.rect.center)
        self.animation_frame = 0
        small_enemies.add(self)

    def update(self, should_animate) -> None:
        self.position += self.velocity
        self.rect.center = self.position
        self.check_hitbox()
        if should_animate: self.animate()

    def receive_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            points.Point(self.position.x, self.position.y, points_sprite)
            self.kill()
    def check_hitbox(self):
        for i in bullets.player_bullets:
            if pygame.Rect.colliderect(self.rect, i.rect):
                i.kill()
                self.receive_damage()

    def animate(self):
        self.animation_frame += 1
        if self.animation_frame >= len(sprites[self.name]):
            self.animation_frame = 0
        frame = self.animation_frame
        self.image = sprites[self.name][frame]

def normal(position_x, position_y):
    SmallEnemy('enemy_marshmellow.txt', position_x, position_y)