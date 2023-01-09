import pygame
from pygame.locals import *
import bullets

pattern = []

class Enemy(object):
    def __init__(self, hp) -> None:
        self.hp = hp
        self.image = pygame.image.load('sprites/enemy.png')
        self.rect = self.image.get_rect(center=(1200 / 2 , 800 / 2))
        self.position = self.rect.center
    
    def ring(self, number_of_bullets: int, bullet_speed: int,  offset_angle: int = 0) -> None:
        angle = 360/number_of_bullets
        for i in range(number_of_bullets):
            bullets.Bullet(angle*i + offset_angle, bullet_speed, self.position)
    def spiral(_self, number_of_bullets, bullet_speed, amount, delay):
        for i in range(amount):
            pattern.append({'ring': {'bullets': number_of_bullets, 'speed': bullet_speed, 'offset': i * 10}})
            pattern.append({ 'wait': delay })

    def activate_spell_card(self) -> None:
        pattern.append({ 'wait': 2000 })
        spellcard = open('spell_card.txt')
        for i in spellcard:
            try: 
                attack = eval(i)
                for key, data in attack.items():
                    match key:
                        case 'spiral':
                            self.spiral(data[0], data[1], data[2], data[3])
                        case 'ring':
                            for _ in range(data[3]):
                                pattern.append({'ring': {'bullets': data[0], 'speed': data[1],
                                                        'offset': data[2]}})
                                pattern.append({'wait': data[4]})
                        case 'wait':
                            pattern.append({ 'wait': data })
            except:
                print('IT DOWN BAAD MAN')

    def applyPattern(self):
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
        except IndexError:
            self.activate_spell_card()