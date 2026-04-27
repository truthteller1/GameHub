import pygame
from games.text import Text

class Button:                                                                                                            
    def __init__(self,location,screen,color=(100,100,0),border_color=(255,255,255),img=None,size = (160,50),border_radius = None,border_width=5):#text=None,fontsize=None,font="calibri",text_color=white
        # if type:
        #     self.type = "text"
        #     #self.text_surf = create_textsurf(text,fontsize,font,text_color,bg_color)
        #     self.text_rect = self.text_surf.get_rect(center = self.location)
        #     self.rect = pygame.Rect(location[0]-size[0]/2,location[1]-size[1]/2,size[0],size[1])

        # else:
        #     self.type = "img"
        #     self.img = pygame.image.load(img).convert_alpha()
        #     self.rect = self.img.get_rect(center=self.location)
        self.screen = screen
        self.location = location
        self.size = size
        self.uh = False
        self.assigned = False
        self.scale=1
        self.border_width = border_width
        self.active = True
        if img:
            self.img = pygame.transform.smoothscale(pygame.image.load(img).convert_alpha(),size)
            self.og_img = self.img
            self.rect = self.img.get_rect(center=location)
        else:
            self.img = None
            self.color = color
            self.border_color = border_color
            self.rect = pygame.Rect(location[0]-size[0]/2,location[1]-size[1]/2,size[0],size[1])
            if not border_radius:
                self.border_radius = size[1]//2
            else:
                self.border_radius = border_radius
        self.nrect=self.rect
        self.osize = self.size

    def render(self):
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos()) and not(pygame.mouse.get_pressed()[0])
        if self.active:
            if self.hover and not(self.uh):
                self.size = (self.osize[0]*1.2,self.osize[1]*1.05)
                self.nrect = pygame.Rect(self.location[0]-self.size[0]/2,self.location[1]-self.size[1]/2,self.size[0],self.size[1])
                if self.img:
                    self.img = pygame.transform.smoothscale_by(self.og_img,1.2)
                self.scale=1.05

            if self.uh and not(self.hover):
                self.size = self.osize
                self.nrect = self.rect
                if self.img:
                    self.img = self.og_img
                self.scale=1
        else:
            self.nrect = self.rect
        if self.img:
            self.screen.blit(self.img,self.nrect)
        else:
            pygame.draw.rect(self.screen,self.color,self.nrect,self.border_width,self.border_radius)

        if self.assigned:
            self.text.render(self.scale)

        self.uh = self.hover

    def assigntext(self,text,fontsize,font="calibri",text_color=(255,255,255)):
        self.assigned = True
        self.text = Text(text,fontsize,self.location,self.screen,font,text_color)
