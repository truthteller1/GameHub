from .game_class import Game
import pygame
import numpy as np

class Chain_rxn(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        self.screen = screen
        self.boardrects = []
        #restructure vars
        bx = 20
        by = 20
        buffer  = 10
        side = 30
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))

    def renderboard(self, dimensions):
        bx = 20
        by = 20
        buffer  = 10
        side = 30
        for i in range(self.gameboard.shape[0]):
            #self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                #self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))
                pygame.draw.rect(self.screen, (0,255,0), self.boardrects[i][j])
                #if self.gameboard[i][j] == 1:
                    #REPLACE THIS WITH X
                    #pygame.draw.circle(self.screen,(255,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2)
                #elif self.gameboard[i][j] == 2:
                    #REPLACE WITH O
                    #pygame.draw.circle(self.screen,(0,0,255),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2)

    def make_move(self, move):
        if self.gameboard[move][1] == 0:
            self.gameboard[move] = [self.rep[self.turn],1]
        elif (move == (0,0) or move == (self.gameboard.shape[0] - 1,0) or move == (0, self.gameboard.shape[1] - 1) or move == (self.gameboard.shape[0] - 1, self.gameboard.shape[1] - 1)) and self.gameboard[move][1] == 1:
            self.gameboard[move] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if move[0] + i >=0 and move[0] + i < self.gameboard.shape[0] and move[1] + j >= 0 and move[1] + j < self.gameboard.shape[1] and (i != 0 or j != 0) and (i == 0 or j == 0):
                        self.gameboard[move[0] + i, move[1] + j, 0] = self.rep[self.turn]
                        self.make_move((move[0] + i, move[1] + j))
        elif move[0] * move[1] * (move[0] - self.gameboard.shape[0] + 1) * (move[1] - self.gameboard.shape[1] + 1) == 0 and self.gameboard[move][1] == 2:
            self.gameboard[move] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if move[0] + i >=0 and move[0] + i < self.gameboard.shape[0] and move[1] + j >= 0 and move[1] + j < self.gameboard.shape[1] and (i != 0 or j != 0) and (i == 0 or j == 0):
                        self.gameboard[move[0] + i, move[1] + j, 0] = self.rep[self.turn]
                        self.make_move((move[0] + i, move[1] + j))
        elif self.gameboard[move][1] == 3:
            self.gameboard[move] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if move[0] + i >=0 and move[0] + i < self.gameboard.shape[0] and move[1] + j >= 0 and move[1] + j < self.gameboard.shape[1] and (i != 0 or j != 0) and (i == 0 or j == 0):
                        self.gameboard[move[0] + i, move[1] + j, 0] = self.rep[self.turn]
                        self.make_move((move[0] + i, move[1] + j))
        else:
            self.gameboard[move][1] += 1

    def checkpress(self,click):
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if (self.boardrects[i][j]).collidepoint(click.pos) and (self.gameboard[i][j][0] == self.rep[self.turn] or self.gameboard[i,j,0] == 0):
                    self.make_move((i,j))
                    print(self.gameboard)
                    if self.check_win_condition((i,j)) != 0:
                        return True
                    self.switch_turn()

    def check_win_condition(self, move):
        if np.argwhere(self.gameboard[:,:,0] == self.rep[self.turn]).size != 2 and np.argwhere(self.gameboard[:,:,0] == 3 - self.rep[self.turn]).size == 0:
            return self.rep[self.turn]
        else:
            return 0
