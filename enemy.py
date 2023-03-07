import pygame
from pygame.locals import *
from pygame.math import Vector2
import bullets
import math

pattern = []
tracking_bullets = []

class Enemy(object):
    def __init__(self, hp, name) -> None:
        self.hp = hp
        self.pattern = f'data/spell_cards/{name}.txt'
        self.image = pygame.image.load(f'sprites/{name}_boss.png')
        self.rect = self.image.get_rect(center=(800 / 2 , -50))
        self.position = self.rect.center

    def check_hitbox(self, player):
        if self.hp > 0 and self.rect.center[1] < 400:
            self.rect.y += 5
            self.position = self.rect.center
        else:
            for i in bullets.player_bullets:
                if pygame.Rect.colliderect(self.rect, i.rect):
                    i.kill()
                    self.receive_damage(player)

    def receive_damage(self, player):
        self.hp -= 1
        if self.hp == 0:
            player.points += 100000
    
    def ring(self, number_of_bullets: int, bullet_speed: int,  offset_angle: int = 0) -> None:
        angle = 360/number_of_bullets
        for i in range(number_of_bullets):
            bullets.Bullet(angle*i + offset_angle, bullet_speed, self.position)

    def tracking(self, number_of_bullets, bullet_speed):
        if number_of_bullets == 1:
            tracking_bullets.append(bullets.Bullet(0,bullet_speed, (self.position[0], self.position[1] + 50)))
        else:
            angle = 360 / number_of_bullets
            for i in range(number_of_bullets):
                pos_x = self.position[0] + 50 * math.cos(math.radians(angle * i))
                pos_y = self.position[1] + 50 * math.sin(math.radians(angle * i))
                tracking_bullets.append(bullets.Bullet(0,bullet_speed, (pos_x, pos_y)))

    def fire_tracking(self, speed, player):
        global tracking_bullets
        
        for i in tracking_bullets:
            i.velocity = Vector2(0.1 * speed, 0).rotate(math.degrees(math.atan2(player.hitbox[1] - i.pos[1], player.hitbox[0] - i.pos[0]))) * 5
        tracking_bullets = []

    def spiral(_self, number_of_bullets, bullet_speed, amount, delay, direction):
        for i in range(amount):
            pattern.append({'ring': {'bullets': number_of_bullets, 'speed': bullet_speed, 'offset': i * direction * 10}})
            pattern.append({ 'wait': delay })

    def activate_spell_card(self) -> None:
        pattern.append({ 'wait': 2000 })
        spellcard = open(self.pattern)
        for i in spellcard:
            try: 
                if i:
                    attack = eval(i)
                    for key, data in attack.items():
                        match key:
                            case 'spiral':
                                self.spiral(data[0], data[1], data[2], data[3], data[4])
                            case 'ring':
                                for _ in range(data[3]):
                                    pattern.append({'ring': {'bullets': data[0], 'speed': data[1],
                                                            'offset': data[2]}})
                                    pattern.append({'wait': data[4]})
                            case 'tracking':
                                for _ in range(data[2]):
                                    pattern.append({'tracking': {'bullets': data[0], 'speed': 0}})
                                    pattern.append({'wait': data[3]})
                                    pattern.append({'fire_tracking' : data[1]})
                            case 'wait':
                                pattern.append({ 'wait': data })
            except:
                print('IT DOWN BAD MAN')

    def applyPattern(self, player):
        try:
            item = pattern[0]
            for key, value in item.items():
                match key:
                    case 'ring':
                        self.ring(value.get('bullets'), value.get('speed'), value.get('offset'))
                        pattern.pop(0)
                    case 'wait':
                        if value <= 0:
                            pattern.pop(0)
                        else:
                            item['wait'] -= 50
                    case 'tracking':
                        self.tracking(value.get('bullets'), value.get('speed'))
                        pattern.pop(0)
                    case 'fire_tracking':
                        self.fire_tracking(value, player)
                        pattern.pop(0)
        except IndexError:
            self.activate_spell_card()