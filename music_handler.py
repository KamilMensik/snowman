import pygame
from pygame import mixer

mixer.init()

songs = {
    'LoliPopJam' : { 'format' : 'mp3', 'volume' : 1},
    'Menu_Theme' : { 'format' : 'mp3', 'volume' : 1},
    'Septette_for_the_dead_Snowman' : { 'format' : 'mp3', 'volume' : 1},
    'Talking' : { 'format' : 'mp3', 'volume' : 1}
}
class MusicHandler():
    def __init__(self) -> None:
        self.song = False
        self.fadeout = 0
        self.in_queue = False

    def play_music(self, volume):
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.set_volume(volume)
        mixer.music.play(-1)

    def tick(self):
        if self.fadeout > 0:
            self.fadeout -= 1
            if self.fadeout == 0:
                mixer.music.unload()
                self.song = self.in_queue[0]
                self.play_music(self.in_queue[1])

    def change_music(self, song_name):
        path = f'sounds/songs/{song_name}.{songs[song_name]["format"]}'
        volume = songs[song_name]['volume']

        if self.song:
            mixer.music.fadeout(500)
            self.fadeout = 45
            self.in_queue = [path, volume]
        else:
            self.song = path
            self.play_music(volume)

    def stop_music(self):
        mixer.music.stop()
