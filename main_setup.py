import sys, pygame
from pygame.locals import *
from player import Player
from enemy import Enemy
from enum import Enum

screens = Enum('Screens', ['GAME', 'CREDITS', 'QUIT', 'MENU'])

class Defaults():
    def __init__(self) -> None:
        self.size = width, height = 1200, 800
        self.BLACK = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        self.player_image = pygame.image.load('sprites/image.gif').convert_alpha()
        self.player = Player(self.player_image, 5)
        self.enemy = Enemy(120)
        self.apply_pattern_event = pygame.USEREVENT + 1
        self.clock = pygame.time.Clock()
        self.current_screen = screens.MENU

def defaults():
    return data

data = Defaults()