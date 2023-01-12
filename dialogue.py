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

class Dialogue():
    def __init__(self, dialogue) -> None:
        self.data = eval('\t'.join([line.strip() for line in open(dialogue).readlines()]))
        self.char_left = Character(self.data[0][0], self.data[0][1], (0, 400))
        self.char_right = Character(self.data[1][0], self.data[1][1], (1000, 400))
        self.text = ''
        self.page = 0
        self.end = False
        self.next_line()

    def next_line(self):
        try:
            line = self.data[self.page+2]
            character = None
            match line.get('side'):
                case 'left':
                    character = self.char_left
                case 'right':
                    character = self.char_right
            character.image = sprites.get(line.get('character')).get(line.get('emotion'))
            self.text = line.get('text')
            self.page += 1
        except IndexError:
            self.end = True

print(sprites)