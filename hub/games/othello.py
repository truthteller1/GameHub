from .game_class import Game
import pygame
import numpy as np

class Othello(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        self.has_moves = np.vectorize(self.valid_move)
        self.screen = screen
        self.boardrects = []
        #restructure vars
        bx = 20
        by = 20
        buffer  = 10
        side = 30
        self.gameboard[3,3] = 1
        self.gameboard[4,4] = 1
        self.gameboard[3,4] = 2
        self.gameboard[4,3] = 2
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))

    def renderboard(self, dimensions):
        bx = 20
        by = 20
        buffer  = 10
        side = 30
        moves = self.possible_moves()
        for i in range(self.gameboard.shape[0]):
            #self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                #self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))
                pygame.draw.rect(self.screen, (0,255,0), self.boardrects[i][j])
                if self.gameboard[i][j] == 1:
                    #REPLACE THIS WITH X
                    pygame.draw.circle(self.screen,(255,255,255),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2)
                elif self.gameboard[i][j] == 2:
                    #REPLACE WITH O
                    pygame.draw.circle(self.screen,(0,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2)
                
        for k in moves:
            i,j=k
            pygame.draw.circle(self.screen,(0,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2,width = 2)

    def check_list(self,arr, pos, player):
        if np.argwhere(arr[:pos] == player).size != 0:
            if not (arr[np.argwhere(arr[:pos] == player)[-1,0]:pos] == 0).any() and np.argwhere(arr[:pos] == player)[-1,0] + 1 != pos:
                return True
        elif np.argwhere(arr[pos:] == player).size != 0:
            if not (arr[pos + 1:np.argwhere(arr[pos:] == player)[0,0] + pos + 1] == 0).any() and np.argwhere(arr[pos:] == player)[0,0] != 1:
                return True
        return False

    def valid_move(self,move0,move1,player):
        vert,hor,rdiag,ldiag = False,False,False,False
        idxr = min(move0, move1) #index of played move in the rightways diagonal containing it
        idxl = min(move0, self.gameboard.shape[1] - 1 - move1) #index of played move in the leftways diagonal containing it
        vert = self.check_list(self.gameboard[:,move1],move0,player)
        hor = self.check_list(self.gameboard[move0,:],move1,player)
        rdiag = self.check_list(self.gameboard.diagonal(move1 - move0),idxr,player)
        ldiag = self.check_list(self.gameboard[:,::-1].diagonal(self.gameboard.shape[1] - 1 - move1 - move0),idxl,player)
        if vert or hor or rdiag or ldiag:
            return True
        else:
            return False

    def make_move(self,move):
        idxr = min(move[1],move[0])
        idxl = min(move[0],self.gameboard.shape[1] - 1 - move[1])
        if self.check_list(self.gameboard[:move[0] + 1,move[1]],move[0],self.rep[self.turn]):
            self.gameboard[np.argwhere(self.gameboard[:move[0] + 1,move[1]] == self.rep[self.turn])[-1,0]:move[0],move[1]] = self.rep[self.turn]
        if self.check_list(self.gameboard[move[0]:,move[1]],0,self.rep[self.turn]):
            self.gameboard[move[0] + 1:np.argwhere(self.gameboard[move[0]:,move[1]] == self.rep[self.turn])[0,0] + move[0],move[1]] = self.rep[self.turn]
        if self.check_list(self.gameboard[move[0],:move[1] + 1],move[1],self.rep[self.turn]):
            self.gameboard[move[0],np.argwhere(self.gameboard[move[0],:move[1] + 1] == self.rep[self.turn])[-1,0]:move[1]] = self.rep[self.turn]
        if self.check_list(self.gameboard[move[0],move[1]:],0,self.rep[self.turn]):
            self.gameboard[move[0],move[1] + 1:np.argwhere(self.gameboard[move[0],move[1]:] == self.rep[self.turn])[0,0] + move[1]] = self.rep[self.turn]
        if self.check_list(self.gameboard.diagonal(move[1]-move[0])[:idxr + 1],idxr,self.rep[self.turn]):
            count = 1
            reqidx = np.argwhere(self.gameboard.diagonal(move[1]-move[0])[:idxr] == self.rep[self.turn])[-1,0]
            while min(move[0]-count,move[1]-count) != reqidx:
                self.gameboard[move[0]-count,move[1]-count] = self.rep[self.turn]
                count += 1
        if self.check_list(self.gameboard.diagonal(move[1]-move[0])[idxr:],0,self.rep[self.turn]):
            count = 1
            reqidx = np.argwhere(self.gameboard.diagonal(move[1]-move[0])[idxr:] == self.rep[self.turn])[0,0] + idxr
            while min(move[0]+count,move[1]+count) != reqidx:
                self.gameboard[move[0]+count,move[1]+count] = self.rep[self.turn]
                count += 1
        if self.check_list(self.gameboard[:,::-1].diagonal(self.gameboard.shape[1]-1-move[1]-move[0])[:idxl + 1],idxl,self.rep[self.turn]):
            count = 1
            reqidx = np.argwhere(self.gameboard[:,::-1].diagonal(self.gameboard.shape[1]-1-move[1]-move[0])[:idxl] == self.rep[self.turn])[-1,0]
            while min(move[0]-count,self.gameboard.shape[1]-1-move[1]-count) != reqidx:
                self.gameboard[move[0]-count,move[1]+count] = self.rep[self.turn]
                count += 1
        if self.check_list(self.gameboard[:,::-1].diagonal(self.gameboard.shape[1]-1-move[1]-move[0])[idxl:],0,self.rep[self.turn]):
            count = 1
            reqidx = np.argwhere(self.gameboard[:,::-1].diagonal(self.gameboard.shape[1]-1-move[1]-move[0])[idxl:] == self.rep[self.turn])[0,0] + idxl
            while min(move[0]+count,self.gameboard.shape[1]-1-move[1]+count) != reqidx:
                self.gameboard[move[0]+count,move[1]-count] = self.rep[self.turn]
                count += 1
        self.gameboard[move[0],move[1]] = self.rep[self.turn]

    def possible_moves(self):
        
        return np.argwhere(self.gameboard==0)[self.has_moves(np.argwhere(self.gameboard==0)[:,0],np.argwhere(self.gameboard==0)[:,1],self.rep[self.turn])]

    def checkpress(self,click):
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):

                if (self.boardrects[i][j]).collidepoint(click.pos) and self.gameboard[i][j]==0 and self.valid_move(i,j,self.rep[self.turn]):
                    self.make_move((i,j))
                    if self.check_win_condition((i,j)) != 0:
                        return True
                    self.switch_turn()
                    if not self.has_moves(np.argwhere(self.gameboard == 0).T[[0]],np.argwhere(self.gameboard == 0).T[[1]],self.rep[self.turn]).any():
                        self.switch_turn()
    def check_win_condition(self,move):
        if np.argwhere(self.gameboard == 0).size == 0:
            if np.argwhere(self.gameboard == 1).size == np.argwhere(self.gameboard == 2).size:
                return -1
            elif np.argwhere(self.gameboard == 1).size > np.argwhere(self.gameboard == 2).size:
                return 1
            else:
                return 2
        else:
            if not self.has_moves(np.argwhere(self.gameboard == 0).T[[0]],np.argwhere(self.gameboard == 0).T[[1]],1).any() and not self.has_moves(np.argwhere(self.gameboard == 0).T[[0]],np.argwhere(self.gameboard == 0).T[[1]],2).any():
                if np.argwhere(self.gameboard == 1).size == np.argwhere(self.gameboard == 2).size:
                    return -1
                elif np.argwhere(self.gameboard == 1).size > np.argwhere(self.gameboard == 2).size:
                    return 1
                else :
                    return 2
            else:
                return 0
