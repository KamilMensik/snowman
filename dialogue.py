import pygame
import os
import textwrap

sprites = {}

for i in os.listdir('sprites/for_dialogue'):
    sprites[i] = {}
    for j in os.listdir(f'sprites/for_dialogue/{i}'):
        file_name = os.path.splitext(j)[0]
        sprites[i][file_name] = pygame.image.load(f'sprites/for_dialogue/{i}/{j}').convert_alpha()

dialogue_backgrounds = {}

for i in os.listdir('sprites/dialogue_backgrounds'):
    dialogue_backgrounds[i] = pygame.image.load(f'sprites/dialogue_backgrounds/{i}').convert_alpha()

class Character():
    def __init__(self, character, emotion, position) -> None:
        self.image = sprites.get(character).get(emotion)
        self.rect = self.image.get_rect().move(position)
        self.bounce = 0
        self.offset = 0

    def add_bounce(self):
        self.bounce = 15

    def draw(self, screen):
        if self.offset != self.bounce:
            if self.bounce > 0:
                self.offset += 1
            else:
                self.offset -=1
        elif self.offset == self.bounce and self.bounce != 0:
            self.bounce = 0

        screen.blit(self.image, (self.rect.x, self.rect.y - self.offset))

class Dialogue():
    def __init__(self) -> None:
        self.data = eval('\t'.join([line.strip() for line in open('dialogues.txt').readlines()]))
        self.char_left = Character(self.data[0][0][0], self.data[0][0][1], (0, 400))
        self.char_right = Character(self.data[0][1][0], self.data[0][1][1], (800, 400))
        self.text = ''
        self.char_name = ''
        self.level = 0
        self.page = 0
        self.end = False
        self.background = dialogue_backgrounds['snowy_plain.jpg']

    def next_line(self):
        try:
            line = self.data[self.level][self.page+2]
            character = None
            if line.get('background'):
                self.background = dialogue_backgrounds[line.get('background')]
                self.page +=1
                self.next_line()
            else: 
                match line.get('side'):
                    case 'left':
                        character = self.char_left
                    case 'right':
                        character = self.char_right
                character.image = sprites.get(line.get('character')).get(line.get('emotion'))
                if line.get('character') != 'blank':
                    self.char_name = line.get('character')
                    character.add_bounce()
                    self.text = textwrap.wrap(line.get('text'), 40, break_long_words=False)
                self.page += 1
        except IndexError:
            self.end = True

    def setup(self):
        self.char_left.image = sprites.get(self.data[self.level][0][0]).get(self.data[self.level][0][1])
        self.char_right.image = sprites.get(self.data[self.level][1][0]).get(self.data[self.level][1][1])
        self.next_line()