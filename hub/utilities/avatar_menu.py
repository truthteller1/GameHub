import pygame
import os
from .button import *

class Avatar:
    def __init__(self,SW,SH,screen):
        self.avatar_iter = 0
        self.avatar_quit = Button((SW/2,SH/2+280),screen,color=(8, 69, 4),border_width=0,size=(350,50))
        self.avatar_quit.assigntext("DONE",30,None,(255,0,0))
        self.avatar_buttons = []
        for i in range(10):
            self.avatar_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-180+90*(i//2)),screen,color=(8, 69, 4),border_width=0,size=(40,90)))
            if i % 2 == 0:
                self.avatar_buttons[-1].assigntext("<",30,None)
            else:
                self.avatar_buttons[-1].assigntext(">",30,None)

    def interact(self,event,avatar_data):
        if self.avatar_buttons[0].rect.collidepoint(event.pos):
            self.avatar_iter = (self.avatar_iter - 1) % 2
        elif self.avatar_buttons[1].rect.collidepoint(event.pos):
            self.avatar_iter = (self.avatar_iter + 1) % 2
        elif self.avatar_buttons[2].rect.collidepoint(event.pos):
            avatar_data[self.avatar_iter][1] = (avatar_data[self.avatar_iter][1] - 1) % 5
        elif self.avatar_buttons[3].rect.collidepoint(event.pos):
            avatar_data[self.avatar_iter][1] = (avatar_data[self.avatar_iter][1] + 1) % 5
        elif self.avatar_buttons[4].rect.collidepoint(event.pos):
            avatar_data[self.avatar_iter][2] = (avatar_data[self.avatar_iter][2] - 1) % 5
        elif self.avatar_buttons[5].rect.collidepoint(event.pos):
            avatar_data[self.avatar_iter][2] = (avatar_data[self.avatar_iter][2] + 1) % 5
        elif self.avatar_buttons[6].rect.collidepoint(event.pos):
            avatar_data[self.avatar_iter][3] = (avatar_data[self.avatar_iter][3] - 1) % 5
        elif self.avatar_buttons[7].rect.collidepoint(event.pos):
            avatar_data[self.avatar_iter][3] = (avatar_data[self.avatar_iter][3] + 1) % 5
        elif self.avatar_buttons[8].rect.collidepoint(event.pos):
            avatar_data[self.avatar_iter][4] = (avatar_data[self.avatar_iter][4] - 1) % 5
        elif self.avatar_buttons[9].rect.collidepoint(event.pos):
            avatar_data[self.avatar_iter][4] = (avatar_data[self.avatar_iter][4] + 1) % 5
        elif self.avatar_quit.rect.collidepoint(event.pos):
            os.system(f"sed -i 's/{avatar_data[0][0]}\\t\\(.*\\)\\t.\\t.\\t.\\t./{avatar_data[0][0]}\\t\\1\\t{avatar_data[0][1]}\\t{avatar_data[0][2]}\\t{avatar_data[0][3]}\\t{avatar_data[0][4]}/' users.tsv")
            os.system(f"sed -i 's/{avatar_data[1][0]}\\t\\(.*\\)\\t.\\t.\\t.\\t./{avatar_data[1][0]}\\t\\1\\t{avatar_data[1][1]}\\t{avatar_data[1][2]}\\t{avatar_data[1][3]}\\t{avatar_data[1][4]}/' users.tsv")
            return True
