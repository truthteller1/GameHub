from .game_class import Game
from .avatar_render import *
import pygame
from .text import Text
from pathlib import Path

button = Path(__file__).parent.parent.parent / "Graphics" / "theme_designs"

class TicTacToe(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        
        self.screen = screen
        self.boardrects = []

        # size parameters of gameboard
        bx = 500-250
        by = 150
        buffer  = 6
        side = 44
        
        # setting variables needed for rendering avatars
        self.background = pygame.transform.smoothscale(pygame.image.load(button / "sharprect.png"),((50*self.gameboard.shape[0]+5)*968//800,(50*self.gameboard.shape[1]+5)*968//800))
        self.bgrect = self.background.get_rect()
        self.bgrect.center = (bx+50*5-3,by+50*5-3)
        self.avim = pygame.transform.smoothscale(pygame.image.load(button / "roundrect.png"),(180*968//800,320*968//800))
        self.avrect1 = pygame.Rect(0,0,180*968//800,320*968//800)
        self.avrect1.midtop = (130,180)
        self.avrect2 = pygame.Rect(0,0,180*968//800,320*968//800)
        self.avrect2.midtop = (1000-130,180)
        self.text1 = Text(self.p1,20,(130,500),screen,color=(189,255,209))
        self.text2 = Text(self.p2,20,(1000-130,500),screen,color=(189,255,209))

        # setting rects at each square of the gameboard
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))
        
        self.avatars = {self.p1:parse_avatar(p1),self.p2: parse_avatar(p2)}

    # for rendering gameboard 
    def renderboard(self, dimensions):
        
        bx = 500-250
        by = 150
        buffer  = 6
        side = 44
        
        # renders background of board and each square of the board
        self.screen.blit(self.background,self.bgrect)
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                
                pygame.draw.rect(self.screen, (0,150,0), self.boardrects[i][j])
                if self.gameboard[i][j] == 1:
                    pygame.draw.circle(self.screen,(190,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2-2)
                elif self.gameboard[i][j] == 2:
                    pygame.draw.circle(self.screen,(0,0,190),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2-2)
        
        # rendering both players' avatars (along with which piece is whose)
        Text("Your turn!",60,(500 + ((-1)**(self.rep[self.turn]))*375,180),self.screen,color=(189,255,209)).render() 
        self.screen.blit(self.avim,self.avrect1)
        self.screen.blit(self.avim,self.avrect2)
        self.text1.render(scale = 1+ 0.1*(self.rep[self.turn]%2))
        self.text2.render(scale = 1+ 0.1*(self.rep[self.turn]//2))
        self.renderav((125,300),self.p1)
        pygame.draw.circle(self.screen,(190,0,0),(125,250),15)
        self.renderav((1000-125,300),self.p2)
        pygame.draw.circle(self.screen,(0,0,190),(1000-125,250),15)
    
    # for event handling in game screen
    def checkpress(self,click):
        
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                
                if (self.boardrects[i][j]).collidepoint(click.pos) and self.gameboard[i][j]==0:
                    self.make_move((i,j))
                    if self.check_win_condition((i,j)) != 0:
                        return self.check_win_condition((i,j))
                    self.switch_turn()

    def check_win_condition(self, move):
        
        # slicing each column, row and diagonal through the square where move was played
        vert = self.gameboard[:,move[1]]
        hor = self.gameboard[move[0],:]
        rdiag = self.gameboard.diagonal(move[1] - move[0])
        ldiag = self.gameboard[:,::-1].diagonal(self.gameboard.shape[0] - 1 - move[0] - move[1])

        # checking for 5 in a row (irrespective of boardsize) in each sliced array
        win_vert= ((vert[:-4] == vert[1:-3]) * (vert[:-4] == vert[2:-2]) * (vert[:-4] == vert[3:-1]) * (vert[:-4] == vert[4:]) * (vert[:-4] == self.rep[self.turn])).any()
        
        win_hor= ((hor[:-4] == hor[1:-3]) * (hor[:-4] == hor[2:-2]) * (hor[:-4] == hor[3:-1]) * (hor[:-4] == hor[4:]) * (hor[:-4] == self.rep[self.turn])).any() 
        
        win_rdiag= ((rdiag[:-4] == rdiag[1:-3]) * (rdiag[:-4] == rdiag[2:-2]) * (rdiag[:-4] == rdiag[3:-1]) * (rdiag[:-4] == rdiag[4:]) * (rdiag[:-4] == self.rep[self.turn])).any()
        
        win_ldiag= ((ldiag[:-4] == ldiag[1:-3]) * (ldiag[:-4] == ldiag[2:-2]) * (ldiag[:-4] == ldiag[3:-1]) * (ldiag[:-4] == ldiag[4:]) * (ldiag[:-4] == self.rep[self.turn])).any()

        
        if win_vert or win_hor or win_rdiag or win_ldiag:
            self.winner = self.rep[self.turn]
            return self.rep[self.turn]
        elif not (self.gameboard == 0).any():
            self.winner = -1
            return -1
        else:
            return 0
