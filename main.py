import sys, pygame
from pygame.locals import *
from main_setup import *
from bullets import Bullet, bullets, player_bullets
from small_enemy import SmallEnemy, small_enemies
from points import points

def level_finish():
    global current_screen
    global key_debounce

    key_debounce = True
    pygame.time.set_timer(key_input_debounce, 400, 1)
    dialog.level += 1
    dialog.page = 0
    dialog.end = False
    MusicHandler.change_music('Talking')
    dialog.setup()
    current_screen = screens.DIALOGUE

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

def dialogue_loop():
    global key_debounce
    global current_screen

    if level.boss:
        level.boss = False

    if dialog.end:
        level.level = dialog.level
        level.iteration = 0
        current_screen = screens.GAME
        match level.level:
            case 0:
                MusicHandler.change_music('Septette_for_the_dead_Snowman')
            case 1:
                MusicHandler.change_music('LoliPopJam')
            case 2:
                MusicHandler.change_music('Volcano_Hottape')

    else:
        screen.blit(dialog.background, (0,0))
        if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and key_debounce == False :
            key_debounce = True
            dialog.next_line()
            pygame.time.set_timer(key_input_debounce, 250, 1)
        dialog.char_left.draw(screen)
        dialog.char_right.draw(screen)
        screen.blit(d_box_image, (250, 575))
        for i, text in enumerate(dialog.text):
            draw_text(text, 30, 600, 650 + (i * 30), 'fonts/Aller_Rg.ttf', True)
        draw_text(dialog.char_name, 15, 340, 597, outline=True)
        draw_text(MusicHandler.falling_text.text, 25, MusicHandler.falling_text.position[0], MusicHandler.falling_text.position[1], 'fonts/Aller_Rg.ttf', True)

def axis(keys) -> list:
    x_axis = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
    y_axis = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
    return [x_axis, y_axis]

def exit_loop():
    global exit_timer

    screen.fill('black')
    draw_text('BYE!', 90, 600, 400)

    exit_timer -= 1

def about_loop():
    global current_screen

    screen.fill('black')
    draw_text('Snowman', 60, 600, 275)
    draw_text('A game by Professionell Gamekrs', 40, 600, 375)
    draw_text('Coding: Kamil Mensik', 30, 600, 475)
    draw_text('Music: Lukas Foniok', 30, 600, 525)
    draw_text('Art: Viktorie Kacorova', 30, 600, 575)
    draw_text('Press space to go back', 20, 200, 775)

    if keys[pygame.K_SPACE]:
        current_screen = screens.MENU

def menu_loop():
    global current_screen
    global key_debounce

    if MusicHandler.song != 'sounds/songs/Menu_Theme.mp3':
        MusicHandler.change_music('Menu_Theme')

    screen.blit(menu_image, (0,0))
    screen.blit(menu_char_image, (100, 100))
    handle_menu_selection(y_axis)
    pygame.draw.circle(screen, (255, 255, 255), (800, button_pos * 100 + 500), 10, 10)
    draw_text('SNOWMAN', 50, 950, 400)
    draw_text('PLAY', 40, 950, 500)
    draw_text('ABOUT', 40, 950, 600)
    draw_text('QUIT', 40, 950, 700)
    draw_text(MusicHandler.falling_text.text, 25, MusicHandler.falling_text.position[0], MusicHandler.falling_text.position[1], 'fonts/Aller_Rg.ttf', True)
    if keys[pygame.K_RETURN]:
        match button_pos:
            case 0:
                sounds['game_start'].play()
                MusicHandler.change_music('Talking')
                level.level = 0
                level.iteration = 0
                level.game_end = False
                level.end = False
                level.boss = False
                player.health = 3
                player.points = 0
                player.position.center = (400, 750)
                player.barrier = {}
                dialog.level = 0
                dialog.page = 0
                dialog.end = False
                dialog.setup()
                key_debounce = True
                pygame.time.set_timer(key_input_debounce, 400, 1)
                current_screen = screens.DIALOGUE
                for i in bullets:
                    i.kill()
                for i in small_enemies:
                    i.kill()
                for i in points:
                    i.kill()
            case 2:
                sounds['exit'].play()
                current_screen = screens.QUIT
                MusicHandler.stop_music()
            case other:
                sounds['proceed'].play()
                current_screen = screens.ABOUT

def game_loop():
    global focus_timer
    global should_animate
    global should_apply_level
    global can_shoot
    global current_screen

    if player.health == 0:
        current_screen = screens.MENU
        level.boss = False

    if should_apply_level:
        level.apply_spawn()
    if level.level == 0:
        if level.end and len(small_enemies) == 0:
            level_finish()
    else:
        if level.end and level.boss and level.boss.hp <= 0:
            if level.boss.rect.y > 900:
                level.boss = False
                level_finish()
            else:
                level.boss.rect.y += 3
                level.boss.position = level.boss.rect.center
    focus = keys[pygame.K_LSHIFT]
    player.move(x_axis, y_axis, focus)
    if can_shoot:
        can_shoot = False
        pygame.time.set_timer(key_shoot_debounce, 50)
        player.shoot()
    screen.blit(current_game_background, (0,0))
    bullets.update()
    player_bullets.update()
    player.check_hitbox(bullets)
    bullets.draw(screen)
    points.update(player)
    points.draw(screen)
    player_bullets.draw(screen)
    small_enemies.update(should_animate, player)
    small_enemies.draw(screen)
    if level.boss:
        level.boss.check_hitbox(player)
        draw_boss_healthbar(level.boss)
        screen.blit(level.boss.image, level.boss.rect.topleft)
    if focus:
        if focus_timer == 360:
            focus_timer = 0 
        focus_timer += 30
        focus_rect = focus_image.get_rect()
        focus_rect.center = player.position.center
        screen.blit(focus_image, focus_rect)
    if player.barrier != {}:
        circle = pygame.draw.circle(screen, (255, 0, 0), player.barrier['position'], player.barrier['size'], 5)
        for i in bullets:
            if pygame.Rect.colliderect(circle, i.rect):
                i.kill()

    screen.blit(player.image, player.position)
    if focus:
        pygame.draw.circle(screen, (255, 255, 255), player.hitbox, player.hitbox_radius, 5)
        pygame.draw.circle(screen, (255, 0, 0), player.hitbox, player.hitbox_radius, 1)

    screen.fill("BLACK", (800, 0, 400, 800))
    draw_text(f"Points: {player.points}", 20, 1000, 200)
    draw_health(player, 1000, 100)
    draw_combo(player, 1000, 300)
    draw_text(MusicHandler.falling_text.text, 25, MusicHandler.falling_text.position[0], MusicHandler.falling_text.position[1], 'fonts/Aller_Rg.ttf', True)

while exit_timer > 0:
    should_animate = False
    should_apply_level = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if level.boss and level.boss.hp > 0:
            if event.type == apply_pattern_event and current_screen == screens.GAME: level.boss.applyPattern(player)
        if event.type == key_input_debounce: key_debounce = False
        if event.type == small_enemy_animation_event: should_animate = True
        if event.type == key_shoot_debounce: can_shoot = True
        if event.type == apply_level_event: should_apply_level = True
    keys = pygame.key.get_pressed()
    x_axis, y_axis = axis(keys)

    screen.fill("BLUE")
    MusicHandler.tick()

    if level.game_end:
        current_screen = screens.MENU
        level.game_end = False

    if level.change_background:
        current_game_background = game_backgrounds[level.change_background]
        level.change_background = False

    match current_screen:
        case screens.GAME:
            game_loop()
        case screens.MENU:
            menu_loop()
        case screens.DIALOGUE:
            dialogue_loop()
        case screens.QUIT:
            exit_loop()
        case screens.ABOUT:
            about_loop()
    pygame.display.flip()
    clock.tick(90)