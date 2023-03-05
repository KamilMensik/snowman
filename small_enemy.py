import pygame
from pygame.locals import *
from pygame.math import Vector2
import bullets
import math
import os
import points
import copy
small_enemies = pygame.sprite.Group()
sprites = {}
points_sprite = pygame.image.load('sprites/score.png').convert_alpha()
hit = pygame.mixer.Sound('sounds/hit.wav')
kill = pygame.mixer.Sound('sounds/kill.wav')
attack = pygame.mixer.Sound('sounds/shoot.wav')
enemies_data = eval('\t'.join([line.strip() for line in open('enemies.txt').readlines()]))

for i in os.listdir('sprites/small_enemies'):
    sprites[i] = []
    for j in os.listdir(f'sprites/small_enemies/{i}'):
        sprites[i].append(pygame.image.load(f'sprites/small_enemies/{i}/{j}').convert_alpha())

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, name, position_s, position_f, type= 'normal') -> None:
        pygame.sprite.Sprite.__init__(self)
        data = copy.deepcopy(enemies_data.get(name))
        self.hp = data.get('hp')
        self.finish_pos = position_f
        self.velocity = Vector2(0.1 * data.get('speed'), 0).rotate(math.degrees(math.atan2((position_f[1] - position_s[1]), position_f[0] - position_s[0]))) * 5
        self.attacks = data.get('attacks')
        self.delay = data.get('delay')
        self.name = data.get('name')
        self.points = data.get('points')
        self.image = sprites[self.name][0]
        self.rect = self.image.get_rect()
        self.position = Vector2(position_s)
        self.animation_frame = 0
        self.finished_moving = False
        self.attack_delay = 0
        self.type = type
        small_enemies.add(self)

    def attack(self):
        match self.attacks[0]:
            case 'ring':
                self.attacks.pop(0)
                self.ring(15, 4, 0)

    def ring(self, number_of_bullets: int, bullet_speed: int,  offset_angle: int = 0) -> None:
        angle = 360/number_of_bullets
        for i in range(number_of_bullets):
            bullets.Bullet(angle*i + offset_angle, bullet_speed, self.position)

    def update(self, should_animate) -> None:
        self.check_hitbox()
        
        if not self.finished_moving:
            if math.sqrt((self.position.x - self.finish_pos[0]) ** 2 + (self.finish_pos[1] - self.position.y) ** 2) < 5:
                self.finished_moving = True
            self.position += self.velocity
            self.rect.center = self.position
        else:
            match self.type:
                case 'normal':
                    if self.attack_delay <= 0 and self.attacks != []:
                        self.attack_delay = self.delay
                        self.attack()
                        attack.play()
                    elif self.attacks == []:
                        self.position += Vector2(0,5)
                        self.rect.center = self.position
                        if self.position[1] > 850: self.kill()
                    else:
                        self.attack_delay -= 1
                case 'cola':
                    if self.attack_delay <= 0 and self.attacks != []:
                        self.attack_delay = self.delay
                        self.attack()
                        attack.play()
                    elif self.attacks == []:
                        self.kill()
                    else:
                        self.attack_delay -= 1
        if should_animate: self.animate()

    def receive_damage(self):
        self.hp -= 1
        hit.play()
        if self.hp <= 0:
            kill.play()
            for _ in range(self.points):
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

def marshmellow(position_s, position_f):
    SmallEnemy('marshmellow', position_s, position_f)

def cola(position_s, position_f):
    SmallEnemy('cola', position_s, position_f, 'cola')