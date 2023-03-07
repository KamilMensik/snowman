import pygame
from pygame.locals import *
import bullets
import math

pygame.mixer.init()

class Player(object):
    def __init__(self, image, speed) -> None:
        self.image = image
        self.speed = speed
        self.position = image.get_rect().move(0, 0)
        self.hitbox = (self.position.center)
        self.hitbox_radius = 6
        self.points = 0
        self.health = 3
        self.barrier = {}
        self.combo = [1, 75]
        self.death_wait = 0

    def check_boundaries(self, position, x_axis, y_axis) -> list:
        if x_axis < 0 and position.x <= -25:
            x_axis = 0
        if x_axis > 0 and position.x >= 775:
            x_axis = 0
        if y_axis < 0 and position.y <= -25:
            y_axis = 0
        if y_axis > 0 and position.y >= 775:
            y_axis = 0
        return [x_axis, y_axis]
    
    def check_hitbox(self, projectiles):
        if self.barrier == {}:
            for i in projectiles:
                if math.sqrt((i.pos.x - self.hitbox[0])**2 + (i.pos.y - self.hitbox[1])**2) < i.radius - 1 + self.hitbox_radius:
                    i.kill()
                    self.health -= 1
                    self.barrier = { 'position': self.position.center, 'size': 1}
                    if self.health <= 0:
                        pygame.mixer.Sound('sounds/player_death_sound.mp3').play()
                        self.death_wait = 180
                    else:
                        pygame.mixer.Sound('sounds/player_hit.mp3').play()

    def move(self, x_axis, y_axis, focus) -> None:
        if self.combo[1] > 0:
            self.combo[1] -= 1
            if self.combo[1] <= 0:
                self.combo = [1, 0]
        if focus:
            x_axis /= 1.7
            y_axis /= 1.7
        x_axis, y_axis = self.check_boundaries(self.position, x_axis, y_axis)
        self.position = self.position.move(self.speed * x_axis, self.speed * y_axis)
        self.hitbox = (self.position.center)
        if self.barrier != {}:
            self.barrier['size'] += 5
            if self.barrier['size'] > 250:
                self.barrier = {}
    
    def shoot(self):
        bullets.Bullet(270, 25, self.position.center, type = 'player', sprite = 'sprites/player_bullet.png')