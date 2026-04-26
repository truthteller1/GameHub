from .game_class import Game
from pathlib import Path
import pygame
import numpy as np

class Chain_rxn(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        self.board = self.gameboard
        self.screen = screen
        self.boardrects = []
        self.size = self.screen.get_size()
        #restructure vars
        img_dir = Path(__file__).parent.parent.parent / "Graphics" / "chain_rxn"
        self.buffer  = 10
        self.side = 80
        self.bx = (self.size[0] - self.gameboard.shape[0] * self.side - (self.gameboard.shape[0] - 1) * self.buffer) // 2
        self.by = (self.size[1] - self.gameboard.shape[1] * self.side - (self.gameboard.shape[1] - 1) * self.buffer) // 2
        self.atoms = [[],[]]
        for i in range(2):
            for j in range(3):
                img_path = img_dir / f"atom{i+1},{j+1}.png"
                self.atoms[i].append(pygame.image.load(img_path).convert_alpha())
                self.atoms[i][j] = pygame.transform.scale(self.atoms[i][j],(self.side,self.side))
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((self.bx + j*(self.buffer+self.side),self.by+i*(self.buffer+self.side),self.side,self.side)))

    def renderboard(self, dimensions):
        buffer  = 10
        side = 80
        bx = (self.size[0] - self.gameboard.shape[0] * side - (self.gameboard.shape[0] - 1) * buffer) // 2
        by = (self.size[1] - self.gameboard.shape[1] * side - (self.gameboard.shape[1] - 1) * buffer) // 2

        for i in range(self.gameboard.shape[0]):
            #self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                #self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))
                pygame.draw.rect(self.screen, (0,255,0), self.boardrects[i][j])
                if self.gameboard[i][j][0] != 0:
                    self.screen.blit(self.atoms[self.gameboard[i,j,0] - 1][self.gameboard[i,j,1] - 1],(bx + j*(buffer+side),by+i*(buffer+side)))

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
                        if self.check_win_condition():
                            return
        elif move[0] * move[1] * (move[0] - self.gameboard.shape[0] + 1) * (move[1] - self.gameboard.shape[1] + 1) == 0 and self.gameboard[move][1] == 2:
            self.gameboard[move] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if move[0] + i >=0 and move[0] + i < self.gameboard.shape[0] and move[1] + j >= 0 and move[1] + j < self.gameboard.shape[1] and (i != 0 or j != 0) and (i == 0 or j == 0):
                        self.gameboard[move[0] + i, move[1] + j, 0] = self.rep[self.turn]
                        self.make_move((move[0] + i, move[1] + j))
                        if self.check_win_condition():                                                                                                           return 
        elif self.gameboard[move][1] == 3:
            self.gameboard[move] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if move[0] + i >=0 and move[0] + i < self.gameboard.shape[0] and move[1] + j >= 0 and move[1] + j < self.gameboard.shape[1] and (i != 0 or j != 0) and (i == 0 or j == 0):
                        self.gameboard[move[0] + i, move[1] + j, 0] = self.rep[self.turn]
                        self.make_move((move[0] + i, move[1] + j))
                        if self.check_win_condition():                                                                                                           return 
        else:
            self.gameboard[move][1] += 1

    def checkpress(self,click):
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if ((self.boardrects[i][j]).collidepoint(click.pos)) and ((self.gameboard[i][j][0] == self.rep[self.turn] or self.gameboard[i,j,0] == 0)):
                    self.make_move((i,j))
                    if self.check_win_condition() != 0:
                        return True
                    self.switch_turn()
                    

    def check_win_condition(self):
        if np.argwhere(self.gameboard[:,:,0] == self.rep[self.turn]).size != 2 and np.argwhere(self.gameboard[:,:,0] == 3 - self.rep[self.turn]).size == 0:
            return self.rep[self.turn]
        else:
            return 0
