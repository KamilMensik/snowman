import pygame
import os

sprites = {}

for i in os.listdir('sprites/for_dialogue'):
    sprites[i] = {}
    for j in os.listdir(f'sprites/for_dialogue/{i}'):
        file_name = os.path.splitext(j)[0]
        sprites[i][file_name] = pygame.image.load(f'sprites/for_dialogue/{i}/{j}').convert_alpha()

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
        self.next_line()

    def next_line(self):
        try:
            line = self.data[self.level][self.page+2]
            character = None
            match line.get('side'):
                case 'left':
                    character = self.char_left
                case 'right':
                    character = self.char_right
            character.image = sprites.get(line.get('character')).get(line.get('emotion'))
            self.char_name = line.get('character')
            character.add_bounce()
            self.text = line.get('text')
            self.page += 1
        except IndexError:
            self.end = True