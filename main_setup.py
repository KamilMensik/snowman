# ALL CONSTANTS AND VARIABLES ARE DEFINED HERE

import sys, pygame
from pygame.locals import *
from player import Player
from enemy import Enemy
from enum import Enum

# PYGAME MODULES INITIALIZATIONS
pygame.init()
pygame.mixer.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)

# IMPORTS NEEDED AFTER SCREEN
import dialogue
from levels import Levels, backgrounds

# FUNCTIONS
def draw_text(text, size, x, y):
    font = pygame.font.Font('fonts/04B.TTF', size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_health(player, x, y):
    font = pygame.font.Font('fonts/Segoe UI.ttf', 60, ucs4 = False)
    text_surface = font.render('♡' * player.health, True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# ENUMS
screens = Enum('Screens', ['GAME', 'CREDITS', 'QUIT', 'MENU', 'DIALOGUE'])

# SOUNDS
sounds = { 'browse' : pygame.mixer.Sound('sounds/Browse.wav'),
           'game_start' : pygame.mixer.Sound('sounds/Game_start.wav'),
           'proceed' : pygame.mixer.Sound('sounds/Proceed.wav'),
           'exit' : pygame.mixer.Sound('sounds/Exit.wav') }

# IMAGES
focus_image = pygame.image.load('sprites/focus.png').convert_alpha()
menu_image = pygame.transform.scale(pygame.image.load('sprites/remilia_background.jpg'), (1200, 800))
player_image = pygame.image.load('sprites/image.gif').convert_alpha()

# CONSTANTS
BLACK = 0, 0, 0
clock = pygame.time.Clock()
dialog = dialogue.Dialogue()
level = Levels()

# GAME RELATED
player = Player(player_image, 5)
current_screen = screens.MENU
game_backgrounds = backgrounds
current_game_background = game_backgrounds['forest.jpg']

# Variables
key_debounce = False
button_pos = 0
focus_timer = 0
can_shoot = True

# EVENTS
apply_pattern_event = pygame.USEREVENT + 1
key_input_debounce = pygame.USEREVENT + 2
small_enemy_animation_event = pygame.USEREVENT + 3
key_shoot_debounce = pygame.USEREVENT + 4
apply_level_event = pygame.USEREVENT + 5

# TIMERS
pygame.time.set_timer(apply_pattern_event, 50)
pygame.time.set_timer(apply_level_event, 50)
pygame.time.set_timer(small_enemy_animation_event, 100)