import pygame
from pathlib import Path

gamehub = Path(__file__).parent.parent.parent

class Text:
    def __init__(self,text,size,pos,screen,font=gamehub / "SpaceMono-Regular.ttf",color=(255,255,255)):
        self.screen = screen
        self.text_font = pygame.font.SysFont(str(font),size)
        self.text_surf = self.text_font.render(text,True,color)
        self.rect = self.text_surf.get_rect(center = pos)
        self.pos = pos
    def render(self,scale=1):
        if scale != 1:
            t=pygame.transform.smoothscale_by((self.text_surf),scale)
            trect = t.get_rect(center=self.pos)
            self.screen.blit(t,trect)
        else:
            self.screen.blit(self.text_surf,self.rect)
