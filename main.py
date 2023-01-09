import sys, pygame
from pygame.locals import *
from player import Player
from main_setup import defaults, screens
import bullets

pygame.init()

# Variables
d = defaults()
screen = d.screen
player = d.player
enemy = d.enemy
apply_pattern_event = d.apply_pattern_event
key_input_debounce = pygame.USEREVENT + 2
key_debounce = False
clock = d.clock
pygame.time.set_timer(apply_pattern_event, 50)
button_pos = 0

def handle_menu_selection(y_axis):
    global key_debounce
    global button_pos

    if y_axis != 0 and key_debounce == False :
        key_debounce = True
        button_pos += y_axis
        if button_pos < 0: 
            button_pos = len(screens) -2
        if button_pos > len(screens) -2:
            button_pos = 0
        pygame.time.set_timer(key_input_debounce, 150, 1)

def draw_text(text, size, x, y):
    font = pygame.font.Font('fonts/04B.TTF', size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def axis(keys) -> list:
    x_axis = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
    y_axis = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
    return [x_axis, y_axis]

def game_loop():
    focus = keys[pygame.K_LSHIFT]
    player.move(x_axis, y_axis, focus)
    player.check_hitbox(bullets.getBullets())
    bullets.getBullets().update()
    bullets.getBullets().draw(screen)
    screen.blit(player.image, player.position)
    screen.blit(enemy.image, enemy.rect.topleft)
    if focus:
        pygame.draw.circle(screen, (255, 0, 0), player.hitbox, player.hitbox_radius, 2)
        pygame.draw.circle(screen, (255, 255, 255), player.hitbox, player.hitbox_radius - 1, 5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == apply_pattern_event: enemy.applyPattern()
        if event.type == key_input_debounce: key_debounce = False
    keys = pygame.key.get_pressed()
    x_axis, y_axis = axis(keys)

    screen.fill(d.BLACK)

    match d.current_screen:
        case screens.GAME:
            game_loop()
        case screens.MENU:
            handle_menu_selection(y_axis)
            pygame.draw.circle(screen, (255, 255, 255), (400, button_pos * 100 + 200), 10, 10)
            draw_text('MAIN MENU', 50, 600, 100)
            draw_text('PLAY', 40, 600, 200)
            draw_text('ABOUT', 40, 600, 300)
            draw_text('QUIT', 40, 600, 400)
    pygame.display.flip()
    clock.tick(90)