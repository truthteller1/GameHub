from .game_class import Game
from .avatar_render import *
import pygame

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
        
        # setting rects at each square in the game board
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))
        
        self.avatars = {self.p1:parse_avatar(p1),self.p2: parse_avatar(p2)}

    # for rendering avatars of both players with appropriate opacities based on turn
    def renderav(self, pos, player):
        if self.turn != player:
            transparency = 180
        else:
            transparency = 255
        avatar_render(self.avatars[player],pos,self.screen,transparency,0.4)

    # for rendering game board
    def renderboard(self, dimensions):
        
        bx = 500-250
        by = 150
        buffer  = 6
        side = 44

        # rendering both players' moves on board
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                
                pygame.draw.rect(self.screen, (0,150,0), self.boardrects[i][j])
                if self.gameboard[i][j] == 1:
                    pygame.draw.circle(self.screen,(190,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2-2)
                elif self.gameboard[i][j] == 2:
                    pygame.draw.circle(self.screen,(0,0,190),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2-2)
        
        # rendering both players' avatars (along with which piece is whose)
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
