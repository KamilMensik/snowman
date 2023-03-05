from small_enemy import marshmellow, cola
import pygame, os

leveldata = data = eval('\t'.join([line.strip() for line in open('levels.txt').readlines()]))
backgrounds = {}

for i in os.listdir('sprites/backgrounds'):
    backgrounds[i] = pygame.image.load(f'sprites/backgrounds/{i}').convert_alpha()

class Levels():
    def __init__(self) -> None:
        self.level = 0
        self.iteration = 0
        self.wait = 0
        self.end = False
        self.game_end = False
        self.change_background = False
    
    def apply_spawn(self):
        if self.wait > 0:
            self.wait -= 50
        else :
            try:
                for key, value in leveldata[self.level][self.iteration].items():
                    match key:
                        case 'background':
                            self.change_background = value
                            self.iteration += 1
                        case 'marshmellow':
                            marshmellow(value[0], value[1])
                            self.iteration += 1
                        case 'cola':
                            cola(value[0], value[1])
                            self.iteration += 1
                        case 'wait':
                            self.wait = value
                            self.iteration += 1
            except IndexError:
                if self.level >= len(leveldata):
                    self.game_end = True
                self.end = True