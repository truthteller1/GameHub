from .game_class import Game
from .avatar_render import *
import pygame
import numpy as np

class Connect4(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        self.screen = screen
        self.boardrects = []
        #restructure vars
        bx = 500-210
        by = 190
        buffer  = 6
        side = 54
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))
        self.avatars = {self.p1:parse_avatar(p1),self.p2: parse_avatar(p2)}

    def renderav(self, pos, player):
        if self.turn != player:
            transparency = 180
        else:
            transparency = 255
        avatar_render(self.avatars[player],pos,self.screen,transparency,0.4)

    def renderboard(self, dimensions):
        bx = 500-210
        by = 190
        buffer  = 6
        side = 54
        for i in range(self.gameboard.shape[0]):
            #self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                #self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))
                pygame.draw.rect(self.screen, (0,150,0), self.boardrects[i][j])
                if self.gameboard[i][j] == 1:
                    #REPLACE THIS WITH X
                    pygame.draw.circle(self.screen,(190,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2-2)
                elif self.gameboard[i][j] == 2:
                    #REPLACE WITH O
                    pygame.draw.circle(self.screen,(0,0,190),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2-2)
        self.renderav((145,300),self.p1)
        pygame.draw.circle(self.screen,(190,0,0),(145,250),15)
        self.renderav((1000-145,300),self.p2)
        pygame.draw.circle(self.screen,(0,0,190),(1000-145,250),15)

    def make_move(self,move):
        if self.turn == self.p1:
            self.gameboard[np.argwhere(self.gameboard[:,move[1]] == 0)[-1],move[1]] = 1
        else:
            self.gameboard[np.argwhere(self.gameboard[:,move[1]] == 0)[-1],move[1]] = 2
        print(self.gameboard)

    def checkpress(self,click):
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if (self.boardrects[i][j]).collidepoint(click.pos) and np.argwhere(self.gameboard[:,j] == 0).size != 0:
                    self.make_move((i,j))
                    if self.check_win_condition((i,j)) != 0:
                        return True
                    self.switch_turn()

    def check_win_condition(self, move):
        vert = self.gameboard[:,move[1]]
        hor = self.gameboard[move[0],:]
        rdiag = self.gameboard.diagonal(move[1] - move[0])
        ldiag = self.gameboard[:,::-1].diagonal(self.gameboard.shape[0] - 1 - move[0] - move[1])

        win1_vert= ((vert[:-3] == vert[1:-2]) * (vert[:-3] == vert[2:-1]) * (vert[:-3] == vert[3:]) * (vert[:-3] == 1)).any()
        win1_hor= ((hor[:-3] == hor[1:-2]) * (hor[:-3] == hor[2:-1]) * (hor[:-3] == hor[3:]) * (hor[:-3] == 1)).any()
        win1_rdiag= ((rdiag[:-3] == rdiag[1:-2]) * (rdiag[:-3] == rdiag[2:-1]) * (rdiag[:-3] == rdiag[3:]) * (rdiag[:-3] == 1)).any()
        win1_ldiag= ((ldiag[:-3] == ldiag[1:-2]) * (ldiag[:-3] == ldiag[2:-1]) * (ldiag[:-3] == ldiag[3:]) * (ldiag[:-3] == 1)).any()

        win2_vert= ((vert[:-3] == vert[1:-2]) * (vert[:-3] == vert[2:-1]) * (vert[:-3] == vert[3:]) * (vert[:-3] == 2)).any()
        win2_hor= ((hor[:-3] == hor[1:-2]) * (hor[:-3] == hor[2:-1]) * (hor[:-3] == hor[3:]) * (hor[:-3] == 2)).any()
        win2_rdiag= ((rdiag[:-3] == rdiag[1:-2]) * (rdiag[:-3] == rdiag[2:-1]) * (rdiag[:-3] == rdiag[3:]) * (rdiag[:-3] == 2)).any()
        win2_ldiag= ((ldiag[:-3] == ldiag[1:-2]) * (ldiag[:-3] == ldiag[2:-1]) * (ldiag[:-3] == ldiag[3:]) * (ldiag[:-3] == 2)).any()

        if win1_vert or win1_hor or win1_rdiag or win1_ldiag:
            return 1
        elif win2_vert or win2_hor or win2_rdiag or win2_ldiag:
            return 2
        elif not (self.gameboard == 0).any():
            return -1
        else:
            return 0
