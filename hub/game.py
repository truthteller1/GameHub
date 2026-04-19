import pygame
import sys
import time
from games.tictactoe import TicTacToe
from games.connect4 import Connect4
from games.othello import Othello
from games.chain_rxn import Chain_rxn
from games.checkers import Checkers
import csv

white = (255,255,255)
black = (0,0,0)
navy = (1,3,43)
red = (255, 0,0)
orange = (255,165,0)

pygame.init()
clock=pygame.time.Clock()

SW = 1000
SH = 800

screen = pygame.display.set_mode((SW,SH))

screen.fill(white)

class Text:
    def __init__(self,text,size,pos,font="calibri",color=white):
        self.text_font = pygame.font.SysFont(font,size)
        self.text_surf = self.text_font.render(text,True,color)
        self.rect = self.text_surf.get_rect(center = pos)
        self.pos = pos
    def render(self,scale=1):
        if scale != 1:
            t=pygame.transform.smoothscale_by((self.text_surf),scale)
            trect = t.get_rect(center=self.pos)
            screen.blit(t,trect)
        else:
            screen.blit(self.text_surf,self.rect)

class Button:
    def __init__(self,location,color=orange,border_color=white,img=None,size = (160,50),border_radius = None,border_width=5):#text=None,fontsize=None,font="calibri",text_color=white
        # if type:
        #     self.type = "text"
        #     #self.text_surf = create_textsurf(text,fontsize,font,text_color,bg_color)
        #     self.text_rect = self.text_surf.get_rect(center = self.location)
        #     self.rect = pygame.Rect(location[0]-size[0]/2,location[1]-size[1]/2,size[0],size[1])
            
        # else:
        #     self.type = "img"
        #     self.img = pygame.image.load(img).convert_alpha()
        #     self.rect = self.img.get_rect(center=self.location)
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
            screen.blit(self.img,self.nrect)
        else:
            pygame.draw.rect(screen,self.color,self.nrect,self.border_width,self.border_radius)

        if self.assigned:
            self.text.render(self.scale)

        self.uh = self.hover

    def assigntext(self,text,fontsize,font="calibri",text_color=white):
        self.assigned = True
        self.text = Text(text,fontsize,self.location,font,text_color)
        
    # def onclick(self,pos):
    #     if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
    #         self.action()

class MenuBar:
    def __init__(self,bg_color = (59,59,59), size = (800,160)):
        POS = self.pos = (SW/2,SH-100)
        self.size = size
        self.color = bg_color
        self.buttons=[
                Button((POS[0]-size[0]//2+150, POS[1]),color=(8, 69, 4),border_width=0,size=(200,100),border_radius=10),
                Button((SW/2, POS[1]),color=(8, 69, 4),border_width=0,size=(200,100),border_radius=10),
                Button((POS[0]+size[0]//2-150, POS[1]),color=(8, 69, 4),border_width=0,size=(200,100),border_radius=10)
            ]
        self.buttons[0].assigntext("OPTIONS",50,None,(0,255,0))
        self.buttons[1].assigntext("QUIT",50,None,(255,0,0))
        self.buttons[2].assigntext("PLAY",50,None,(0,0,255))
        self.rect = pygame.Rect(0,0,size[0],size[1])
        self.rect.center = POS
        self.active = True

    def render(self):
        pygame.draw.rect(screen,self.color,self.rect,0,20)
        for b in self.buttons:
            b.render()

class SelectionBar:
    def __init__(self,settings):
        self.settings = settings
        POS=self.POS= (SW/2,SH/2)
        if settings:
            self.buttons=[
                Button((SW/2, POS[1]-200+50),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+150),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+250),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+370),color=(8, 69, 4),border_width=0,size=(300,50))
            ]
            self.buttons[0].assigntext("SOUND",30,None)
            self.buttons[1].assigntext("AVATAR",30,None)
            self.buttons[2].assigntext("ANALYTICS",30,None)
            self.buttons[3].assigntext("BACK",30,None,red)
            self.size = (550,400)

        else:
            self.buttons = [
                #Button(True,(SW/2, SH/2 - 30),)
                Button((SW/2, POS[1]-200+50),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+130),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+210),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+290),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+370),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+470),color=(8, 69, 4),border_width=0,size=(300,50))
            ]
            self.buttons[0].assigntext("TicTacToe",30,None)
            self.buttons[1].assigntext("Othello",30,None)
            self.buttons[2].assigntext("Connect4",30,None)
            self.buttons[3].assigntext("Chain Reaction",30,None)
            self.buttons[4].assigntext("Checkers",30,None)
            self.buttons[5].assigntext("BACK",30,None,red)
            self.size = (550,600)
        self.rect = pygame.Rect(0,0,self.size[0],self.size[1])
        self.rect.center = self.POS
    def render(self):
        #render self
        #dark grey rounded rect with neon green border, maybe glow?
        pygame.draw.rect(screen,(59,59,59),self.rect,0,20)
        for b in self.buttons:
            b.render()
        
quit_rect = pygame.Rect(SW/2-40, SH-50 , 80, 40)

font = pygame.font.SysFont(None, 30)
font1 = pygame.font.SysFont("calibri", 50,bold=True)
buttonfont = pygame.font.SysFont( None ,20)

textsurf = buttonfont.render("QUIT", True, white)
textrect = textsurf.get_rect()
textrect.center = (SW/2, SH-30)

gamesurf = font1.render("GameHub", True, white)
gamerect = gamesurf.get_rect()
gamerect.center = (SW/2 , 100)

buttons = [
    #Button(True,(SW/2, SH/2 - 30),)
    # Button((SW/2, 200)), #somebutton
    # Button((SW/2,200+100)),
    # Button((SW/2,200+100*2)),
    # Button((SW/2,200+100*3)),
    # Button((SW/2,200+100*4)),
    Button((SW-50,50),img = "back.png",size = (30,30))
]
# buttons[0].assigntext("TicTacToe",30,None)
# buttons[1].assigntext("Othello",30,None)
# buttons[2].assigntext("Connect4",30,None)
# buttons[3].assigntext("Chain Reaction",30,None)
# buttons[4].assigntext("Checkers",30,None)

gamebuttons= [
    buttons[-1]
    #settings
]

menu=False
game = None

opacity = pygame.Surface((SW,SH))
opacity.fill((84,84,84))
opacity.set_alpha(171)
menubar = MenuBar()

while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (gamebuttons[-1].rect.collidepoint(event.pos) and not menu):
                    if not game:
                        pygame.quit()
                        sys.exit()
                    else:
                        game = False

                if not game and not menu:
                    # if buttons[0].rect.collidepoint(event.pos):
                    #     game = TicTacToe("me","ching","me",(10,10),screen)
                    # elif buttons[1].rect.collidepoint(event.pos):
                    #     game = Othello("me","ching","me",(8,8),screen)
                    # elif buttons[4].rect.collidepoint(event.pos):
                    #     game = Checkers("me","ching","me",(8,8),screen)
                    # elif buttons[3].rect.collidepoint(event.pos):
                    #     game = Chain_rxn("me","Ching","me",(6,6,2),screen)
                    # elif buttons[2].rect.collidepoint(event.pos):
                    #     game = Connect4("me","ching","me",(7,7),screen)
                    if menubar.buttons[0].rect.collidepoint(event.pos):
                        menu = SelectionBar(True)
                        for b in menubar.buttons:
                            b.active = False
                            
                        buttons[-1].active = False
                    elif menubar.buttons[1].rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif menubar.buttons[2].rect.collidepoint(event.pos):
                        menu = SelectionBar(False)
                        for b in menubar.buttons:
                            b.active = False
                        buttons[-1].active = False
                    
                elif game and not menu:
                    if game.checkpress(event):
                        game = False
                        time.sleep(2)
                
                elif not game and menu and menu.settings == False:
                    if menu.buttons[0].rect.collidepoint(event.pos):
                        game = TicTacToe("me","ching","me",(10,10),screen)
                        menu=False
                    elif menu.buttons[1].rect.collidepoint(event.pos):
                        game = Othello("me","ching","me",(8,8),screen)
                        menu=False
                    elif menu.buttons[4].rect.collidepoint(event.pos):
                        game = Checkers("me","ching","me",(8,8),screen)
                        menu=False
                    elif menu.buttons[3].rect.collidepoint(event.pos):
                        game = Chain_rxn("me","Ching","me",(6,6,2),screen)
                        menu=False
                    elif menu.buttons[2].rect.collidepoint(event.pos):
                        game = Connect4("me","ching","me",(7,7),screen)
                        menu=False
                    elif menu.buttons[5].rect.collidepoint(event.pos):
                        menu = False
                        for b in menubar.buttons:
                            b.active = True
                        buttons[-1].active = True
                
                elif not game and menu and menu.settings == True:
                    if menu.buttons[0].rect.collidepoint(event.pos):
                        pass#sound
                    elif menu.buttons[1].rect.collidepoint(event.pos):
                        pass#avatar
                    elif menu.buttons[2].rect.collidepoint(event.pos):
                        pass#analytics
                    elif menu.buttons[3].rect.collidepoint(event.pos):
                        menu = False
                        for b in menubar.buttons:
                            b.active = True
                        buttons[-1].active = True

    screen.fill(navy)

    if not game:
        screen.blit(gamesurf, gamerect)
        for b in buttons:
            b.render()
        menubar.render()
        
    else:
        game.renderboard("fah")
        for b in gamebuttons:
            b.render()

    if menu:
        screen.blit(opacity,(0,0))
        #include settings rendering func here
        menu.render()
        

    clock.tick(60)
    pygame.display.flip()
