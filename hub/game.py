import pygame
import sys
from games.tictactoe import TicTacToe
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

tttcolor = pygame.Rect(SW/2 - 60, SH/2 -30 -25, 120, 50)
othcolor = pygame.Rect(SW/2 - 60, SH/2 + 50 - 25, 120, 50)
c4color = pygame.Rect(SW/2 - 60, SH/2 + 130 -25, 120, 50)

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
                elif tttrect.collidepoint(event.pos):
                    game = TicTacToe("me","ching","me",(10,10),screen)
                if game:
                    game.checkpress(event)
                
    screen.fill(navy)
    x = int(quit_rect.height/2)
    pygame.draw.rect(screen, red, quit_rect, border_radius = x)
    screen.blit(textsurf, textrect)

    if not game:
        pygame.draw.rect(screen, orange, tttcolor, border_radius = int(tttcolor.height/2))
        pygame.draw.rect(screen, orange, othcolor, border_radius = int(othcolor.height/2))
        pygame.draw.rect(screen, orange, c4color, border_radius = int(c4color.height/2))
        screen.blit(gamesurf, gamerect)
        screen.blit(tttsurf, tttrect)
        screen.blit(othellosurf,othellorect)
        screen.blit(connect4surf, connect4rect)
    else:
        game.renderboard("fah")
        pass
    pygame.display.flip()
