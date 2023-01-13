import sys, pygame
from pygame.locals import *
from main_setup import defaults, screens, sounds
from bullets import Bullet, bullets, player_bullets
from small_enemy import SmallEnemy, small_enemies
import dialogue
from levels import Levels

pygame.init()

# Variables
d = defaults()
screen = d.screen
player = d.player
apply_pattern_event = d.apply_pattern_event
key_input_debounce = pygame.USEREVENT + 2
key_shoot_debounce = pygame.USEREVENT + 4
apply_level_event = pygame.USEREVENT + 5
key_debounce = False
clock = d.clock
pygame.time.set_timer(apply_pattern_event, 50)
pygame.time.set_timer(apply_level_event, 50)
pygame.time.set_timer(d.small_enemy_animation_event, 100)
button_pos = 0
focus_timer = 0
can_shoot = True
dialog = dialogue.Dialogue()
level = Levels()

def level_finish():
    dialog.level += 1
    dialog.page = 0
    dialog.end = False
    dialog.next_line()
    d.current_screen = screens.DIALOGUE

def handle_menu_selection(y_axis):
    global key_debounce
    global button_pos

    if y_axis != 0 and key_debounce == False :
        key_debounce = True
        sounds['browse'].play()
        button_pos += y_axis
        if button_pos < 0: 
            button_pos = len(screens) -3
        if button_pos > len(screens) -3:
            button_pos = 0
        pygame.time.set_timer(key_input_debounce, 150, 1)

def draw_text(text, size, x, y):
    font = pygame.font.Font('fonts/04B.TTF', size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def dialogue_loop():
    global key_debounce

    if dialog.end:
        level.level = dialog.level
        level.iteration = 0
        d.current_screen = screens.GAME
    else:
        if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and key_debounce == False :
            key_debounce = True
            dialog.next_line()
            pygame.time.set_timer(key_input_debounce, 250, 1)
        draw_text(dialog.text, 20, 600, 600)
        screen.blit(dialog.char_left.image, dialog.char_left.rect)
        screen.blit(dialog.char_right.image, dialog.char_right.rect)

def axis(keys) -> list:
    x_axis = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
    y_axis = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
    return [x_axis, y_axis]

def game_loop():
    global focus_timer
    global should_animate
    global should_apply_level
    global can_shoot
    if should_apply_level:
        level.apply_spawn()
    if level.level %2 == 0:
        if level.end and len(small_enemies) == 0:
            level_finish()
    focus = keys[pygame.K_LSHIFT]
    player.move(x_axis, y_axis, focus)
    if keys[pygame.K_SPACE] and can_shoot:
        can_shoot = False
        pygame.time.set_timer(key_shoot_debounce, 150)
        player.shoot()
    bullets.update()
    player_bullets.update()
    player.check_hitbox(bullets)
    bullets.draw(screen)
    player_bullets.draw(screen)
    small_enemies.update(should_animate)
    small_enemies.draw(screen)
    if focus:
        if focus_timer == 360:
            focus_timer = 0 
        focus_timer += 30
        focus_rect = d.focus_image.get_rect()
        focus_rect.center = player.position.center
        screen.blit(d.focus_image, focus_rect)
        
    screen.blit(player.image, player.position)
    if focus:
        pygame.draw.circle(screen, (255, 0, 0), player.hitbox, player.hitbox_radius, 2)
        pygame.draw.circle(screen, (255, 255, 255), player.hitbox, player.hitbox_radius - 1, 5)

while True:
    should_animate = False
    should_apply_level = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        #if event.type == apply_pattern_event and d.current_screen == screens.GAME: enemy.applyPattern(player)
        if event.type == key_input_debounce: key_debounce = False
        if event.type == d.small_enemy_animation_event: should_animate = True
        if event.type == key_shoot_debounce: can_shoot = True
        if event.type == apply_level_event: should_apply_level = True
    keys = pygame.key.get_pressed()
    x_axis, y_axis = axis(keys)

    screen.fill(d.BLACK)

    if level.game_end:
        d.current_screen = screens.MENU
        level.game_end = False

    match d.current_screen:
        case screens.GAME:
            game_loop()
        case screens.MENU:
            image = pygame.transform.scale(pygame.image.load('sprites/remilia_background.jpg'), (1200, 800))
            screen.blit(image, (0,0))
            handle_menu_selection(y_axis)
            pygame.draw.circle(screen, (255, 255, 255), (800, button_pos * 100 + 500), 10, 10)
            draw_text('MANHA-TAN', 50, 950, 400)
            draw_text('PLAY', 40, 950, 500)
            draw_text('ABOUT', 40, 950, 600)
            draw_text('QUIT', 40, 950, 700)
            if keys[pygame.K_RETURN]:
                match button_pos:
                    case 0:
                        sounds['game_start'].play()
                        level.level = 0
                        level.iteration = 0
                        dialog.level = 0
                        dialog.page = 0
                        dialog.end = False
                        d.current_screen = screens.DIALOGUE
                    case 2:
                        sounds['exit'].play()
                        d.current_screen = screens.QUIT
                    case other:
                        sounds['proceed'].play()
                        d.current_screen = screens.CREDITS
        case screens.DIALOGUE:
            dialogue_loop()
    pygame.display.flip()
    clock.tick(90)