import pygame
from .button import *
from pathlib import Path

button = Path(__file__).parent.parent.parent / "Graphics" / "theme_designs"

class SoundTrack:
    def __init__(self,filename,songname,SW,SH,screen):
        self.name = songname
        self.filename = filename
        self.volume = 100
        self.text = Text(songname,35,(SW /2, SH / 2 - 140),screen,None,(87,236,115))
    def load(self):
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play(loops=-1)
    def set_volume(self):
        pygame.mixer.music.set_volume(self.volume/100)

class Sound:
    def __init__(self, SW, SH,soundtracks,screen):
        self.sound_iter = 0
        self.soundtracks = soundtracks
        soundtracks[self.sound_iter].load()
        self.sound_quit = Button((SW/2,SH/2+160),screen,img = button / "backbutton.png",size=(340,90))
        self.sound_quit.assigntext("DONE",30,None,(241,95,95))
        self.sound_buttons = []
        for i in range(4):
            if i % 2 == 0:
                self.sound_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-140+90*(i//2)),screen,img=button / "leftbutton.png",border_width=0,size=(65,69),sqrscaling=True))
            else:
                self.sound_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-140+90*(i//2)),screen,img=button / "rightbutton.png",border_width=0,size=(65,69),sqrscaling=True))

    def interact(self,event):
        songs = len(self.soundtracks)
        if self.sound_buttons[0].rect.collidepoint(event.pos):
            self.sound_iter = (self.sound_iter - 1) % songs
            self.soundtracks[self.sound_iter].load()
        elif self.sound_buttons[1].rect.collidepoint(event.pos):
            self.sound_iter = (self.sound_iter + 1) % songs
            self.soundtracks[self.sound_iter].load()
        elif self.sound_buttons[2].rect.collidepoint(event.pos):
            self.soundtracks[self.sound_iter].volume=(self.soundtracks[self.sound_iter].volume-1)%101
            self.soundtracks[self.sound_iter].set_volume()
        elif self.sound_buttons[3].rect.collidepoint(event.pos):
            self.soundtracks[self.sound_iter].volume=(self.soundtracks[self.sound_iter].volume+1)%101
            self.soundtracks[self.sound_iter].set_volume()
        elif self.sound_quit.rect.collidepoint(event.pos):
            return True
