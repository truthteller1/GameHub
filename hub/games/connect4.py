from .game_class import Game
from .avatar_render import *
import pygame
import numpy as np

class Connect4(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        
        self.screen = screen
        self.boardrects = []
        
        # parameters for board size and gap size
        bx = 500-210
        by = 190
        buffer  = 6
        side = 54

        # seting up rects in each square of the gameboard
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))
        
        self.avatars = {self.p1:parse_avatar(p1),self.p2: parse_avatar(p2)}
    
    # for rendering both players' avatars with appropriate opacities based on whose turn it is
    def renderav(self, pos, player):
        if self.turn != player:
            transparency = 180
        else:
            transparency = 255
        avatar_render(self.avatars[player],pos,self.screen,transparency,0.4)

    # for rendering gameboard
    def renderboard(self, dimensions):
        
        bx = 500-210
        by = 190
        buffer  = 6
        side = 54
        
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                
                pygame.draw.rect(self.screen, (0,150,0), self.boardrects[i][j])
                if self.gameboard[i][j] == 1:
                    pygame.draw.circle(self.screen,(190,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2-2)
                elif self.gameboard[i][j] == 2:
                    pygame.draw.circle(self.screen,(0,0,190),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2-2)
        
        # rendering avatars of both players
        self.renderav((145,300),self.p1)
        pygame.draw.circle(self.screen,(190,0,0),(145,250),15)
        self.renderav((1000-145,300),self.p2)
        pygame.draw.circle(self.screen,(0,0,190),(1000-145,250),15)

    # does not play at point of mouseclick rather plays at lowest unoccupied square in the column
    def make_move(self,move):
        self.gameboard[np.argwhere(self.gameboard[:,move[1]] == 0)[-1],move[1]] = self.rep[self.turn]
        
    # for event handling in game screen
    def checkpress(self,click):

        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                
                if (self.boardrects[i][j]).collidepoint(click.pos) and np.argwhere(self.gameboard[:,j] == 0).size != 0:
                    self.make_move((i,j))
                    if self.check_win_condition((np.argwhere(self.gameboard[:,j] != 0)[0,0],j)): # checks win condition where move was played not where mouse was clicked
                        return self.check_win_condition((np.argwhere(self.gameboard[:,j] != 0)[0,0],j))
                    self.switch_turn()

    def check_win_condition(self, move):

        # slicing each row,column and diagonal passign through the square where move was played
        vert = self.gameboard[:,move[1]]
        hor = self.gameboard[move[0],:]
        rdiag = self.gameboard.diagonal(move[1] - move[0])
        ldiag = self.gameboard[:,::-1].diagonal(self.gameboard.shape[0] - 1 - move[0] - move[1])

        # for checking for 4 in a row (irrespective of board size) in each slice
        win_vert= ((vert[:-3] == vert[1:-2]) * (vert[:-3] == vert[2:-1]) * (vert[:-3] == vert[3:]) * (vert[:-3] == self.rep[self.turn])).any()

        win_hor= ((hor[:-3] == hor[1:-2]) * (hor[:-3] == hor[2:-1]) * (hor[:-3] == hor[3:]) * (hor[:-3] == self.rep[self.turn])).any()
        
        win_rdiag= ((rdiag[:-3] == rdiag[1:-2]) * (rdiag[:-3] == rdiag[2:-1]) * (rdiag[:-3] == rdiag[3:]) * (rdiag[:-3] == self.rep[self.turn])).any()
        
        win_ldiag= ((ldiag[:-3] == ldiag[1:-2]) * (ldiag[:-3] == ldiag[2:-1]) * (ldiag[:-3] == ldiag[3:]) * (ldiag[:-3] == self.rep[self.turn])).any()


        if win_vert or win_hor or win_rdiag or win_ldiag:
            self.winner = self.rep[self.turn]
            return self.rep[self.turn]
        elif not (self.gameboard == 0).any():
            self.winner = -1
            return -1
        else:
            return 0
