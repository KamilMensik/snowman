import pygame
from pygame.locals import *
import bullets
import math

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
                if math.sqrt((i.pos.x - self.hitbox[0])**2 + (i.pos.y - self.hitbox[1])**2) < i.radius + self.hitbox_radius:
                    i.kill()
                    self.health -= 1
                    self.barrier = { 'position': self.position.center, 'size': 1}

    def move(self, x_axis, y_axis, focus) -> None:
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
        bullets.Bullet(270, 25, self.position.center, type = 'player')