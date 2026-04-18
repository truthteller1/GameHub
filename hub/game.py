import pygame
import sys
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

SW = 1000
SH = 800

screen = pygame.display.set_mode((SW,SH))

screen.fill(white)

def create_textsurf(text,size,font="calibri",text_rgb=white,bg_rgb=None):
    text_font = pygame.font.SysFont(font,size)
    text_surf = text_font.render(text,True,text_rgb, bg_rgb)
    return text_surf

def create_button(text, size, font, text_rgb=white,bg_rgb=None):
    surf = create_textsurf(text, size, font, text_rgb,bg_rgb)

class Button:
    #type is true for text
    def __init__(self,type,location,action,text=None,fontsize=None,font="calibri",text_color=white,bg_color=None,border_color=white,img=None, size = (120,50)):
        if type:
            self.type = "text"
            self.text_surf = create_textsurf(text,fontsize,font,text_color,bg_color)
            self.text_rect = self.text_surf.get_rect(center = self.location)
            self.rect = pygame.Rect(location[0]-size[0]/2,location[1]-size[1]/2,size[0],size[1])
            
        else:
            self.type = "img"
            self.img = pygame.image.load(img).convert_alpha()
            self.rect = self.img.get_rect(center=self.location)
        self.action = action
        self.location = location
        self.bg_color = bg_color
        self.border_color = border_color
        self.size = size
    
    def render(self):
        if self.type == "img":
            screen.blit(self.img,self.location)
        else:
            pygame.draw.rect(screen,self.bg_color,self.rect,5,(self.rect.height//2))
            screen.blit(self.text_surf,self.text_rect)
    
    def onclick(self,pos):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.action()
            
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

tttsurf = font.render("Tic-Tac-Toe",True,white)
tttrect = tttsurf.get_rect()
tttrect.center = (SW/2, SH/2 - 30)

othellosurf = font.render("Othello",True,white)
othellorect = othellosurf.get_rect()
othellorect.center = (SW/2, SH/2 + 50)

connect4surf = font.render("Connect4",True,white)
connect4rect = connect4surf.get_rect()
connect4rect.center = (SW/2, SH/2 + 130)

chainrxnsurf = font.render("Chain Reaction",True,white)
chainrxnrect = chainrxnsurf.get_rect()
chainrxnrect.center = (SW/2, SH/2 + 210)

checksurf = font.render("Checkers",True,white)
checkrect = checksurf.get_rect()
checkrect.center = (SW/2, SH/2 + 290)


tttcolor = pygame.Rect(SW/2 - 60, SH/2 -30 -25, 120, 50)
othcolor = pygame.Rect(SW/2 - 60, SH/2 + 50 - 25, 120, 50)
c4color = pygame.Rect(SW/2 - 60, SH/2 + 130 -25, 120, 50)

crxncolor = pygame.Rect(SW/2 - 60, SH/2 + 210 - 25, 120, 50)

checkcolor = pygame.Rect(SW/2 - 60, SH/2 + 290 -25, 120, 50)

buttons = [
    #Button(True,(SW/2, SH/2 - 30),)
]
gamebuttons= [

]


game = None

while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if quit_rect.collidepoint(event.pos):
                    if not game:
                        pygame.quit()
                        sys.exit()
                    else:
                        game = False

                if not game:
                    if tttcolor.collidepoint(event.pos):
                        game = TicTacToe("me","ching","me",(10,10),screen)
                    elif othcolor.collidepoint(event.pos):
                        game = Othello("me","ching","me",(8,8),screen)
                    elif checkcolor.collidepoint(event.pos):
                        game = Checkers("me","ching","me",(8,8),screen)
                    elif crxncolor.collidepoint(event.pos):
                        game = Chain_rxn("me","Ching","me",(6,6,2),screen)
                    elif c4color.collidepoint(event.pos):
                        game = Connect4("me","ching","me",(7,7),screen)
                if game:
                    if game.checkpress(event):
                        game = False
                
    screen.fill(navy)
    x = int(quit_rect.height/2)
    pygame.draw.rect(screen, red, quit_rect, border_radius = x)
    screen.blit(textsurf, textrect)

    if not game:
        pygame.draw.rect(screen, orange, tttcolor, border_radius = int(tttcolor.height/2))
        pygame.draw.rect(screen, orange, othcolor, border_radius = int(othcolor.height/2))
        pygame.draw.rect(screen, orange, c4color, border_radius = int(c4color.height/2))
        pygame.draw.rect(screen, orange, crxncolor, border_radius = int(crxncolor.height/2))
        pygame.draw.rect(screen, orange, checkcolor, border_radius = int(c4color.height/2))
        screen.blit(gamesurf, gamerect)
        screen.blit(tttsurf, tttrect)
        screen.blit(othellosurf,othellorect)
        screen.blit(connect4surf, connect4rect)
        screen.blit(chainrxnsurf, chainrxnrect)
        screen.blit(checksurf, checkrect)
        for b in buttons:
            b.render()

    else:
        game.renderboard("fah")
        for b in gamebuttons:
            b.render()
        pass
    pygame.display.flip()
