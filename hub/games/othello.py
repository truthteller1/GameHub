from .game_class import Game
from .avatar_render import *
import pygame
import numpy as np
from .text import Text
from pathlib import Path

button = Path(__file__).parent.parent.parent / "Graphics" / "theme_designs"

class Othello(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        self.has_moves = np.vectorize(self.valid_move)
        self.screen = screen
        self.boardrects = []
        
        # board size, innitial parameters
        bx = 500-240
        by = 160
        buffer  = 4
        side = 56
        self.gameboard[3,3] = 1
        self.gameboard[4,4] = 1
        self.gameboard[3,4] = 2
        self.gameboard[4,3] = 2

        # setting variables for rendering avatar
        self.avatars = {self.p1:parse_avatar(p1),self.p2: parse_avatar(p2)}
        self.background = pygame.transform.smoothscale(pygame.image.load(button / "sharprect.png"),((60*self.gameboard.shape[0]+5)*968//800,(60*self.gameboard.shape[1]+5)*968//800))
        self.bgrect = self.background.get_rect()
        self.bgrect.center = (bx+60*4-2,by+60*4-2)
        self.avim = pygame.transform.smoothscale(pygame.image.load(button / "roundrect.png"),(180*968//800,320*968//800))
        self.avrect1 = pygame.Rect(0,0,180*968//800,320*968//800)
        self.avrect1.midtop = (130,180)
        self.avrect2 = pygame.Rect(0,0,180*968//800,320*968//800)
        self.avrect2.midtop = (1000-130,180)
        self.text1 = Text(self.p1,20,(130,500),screen,color=(189,255,209))
        self.text2 = Text(self.p2,20,(1000-130,500),screen,color=(189,255,209))

        # setting up rects at each square of the gameboard
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))

    # for rendering the game board
    def renderboard(self, dimensions):
        bx = 500-240
        by = 160
        buffer  = 4
        side = 56
        moves = self.possible_moves() # gives a list of all indices where a valid move is present for current player

        # renders the board and its background
        self.screen.blit(self.background,self.bgrect)
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                
                pygame.draw.rect(self.screen, (0,150,0), self.boardrects[i][j])
                if self.gameboard[i][j] == 1:
                    pygame.draw.circle(self.screen,(255,255,255),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2-2)
                elif self.gameboard[i][j] == 2:
                    pygame.draw.circle(self.screen,(0,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2-2)
        
        # indicates which squares have valid moves with a circle
        if moves.size != 0:
            for k in moves:
                i,j=k
                pygame.draw.circle(self.screen,(0,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2-2,width = 2)
        
        # rendering avatars of both players along with their corresponding piece colours
        Text("Your turn!",60,(500 + ((-1)**(self.rep[self.turn]))*375,180),self.screen,color=(189,255,209)).render()
        self.screen.blit(self.avim,self.avrect1)
        self.screen.blit(self.avim,self.avrect2)
        self.text1.render(scale = 1+ 0.1*(self.rep[self.turn]%2))
        self.text2.render(scale = 1+ 0.1*(self.rep[self.turn]//2))
        self.renderav((130,300),self.p1)
        pygame.draw.circle(self.screen,(255,255,255),(130,250),20)
        self.renderav((1000-130,300),self.p2)
        pygame.draw.circle(self.screen,(0,0,0),(1000-130,250),20)
    
    # checks whether the input list has a valid othello move or not
    def check_list(self,arr, pos, player):
        if np.argwhere(arr[:pos] == player).size != 0:
            if not (arr[np.argwhere(arr[:pos] == player)[-1,0]:pos] == 0).any() and np.argwhere(arr[:pos] == player)[-1,0] + 1 != pos:
                return True
        elif np.argwhere(arr[pos:] == player).size != 0:
            if not (arr[pos + 1:np.argwhere(arr[pos:] == player)[0,0] + pos + 1] == 0).any() and np.argwhere(arr[pos:] == player)[0,0] != 1:
                return True
        return False

    # checks if the move played by the player is valid or not
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
        
        # checks if the column containing move played has a valid othello moves and flips opponents pieces accordingly
        if self.check_list(self.gameboard[:move[0] + 1,move[1]],move[0],self.rep[self.turn]):
            self.gameboard[np.argwhere(self.gameboard[:move[0] + 1,move[1]] == self.rep[self.turn])[-1,0]:move[0],move[1]] = self.rep[self.turn]
        if self.check_list(self.gameboard[move[0]:,move[1]],0,self.rep[self.turn]):
            self.gameboard[move[0] + 1:np.argwhere(self.gameboard[move[0]:,move[1]] == self.rep[self.turn])[0,0] + move[0],move[1]] = self.rep[self.turn]

        # checks if the row containing move played has a valid othello moves and flips opponents pieces accordingly 
        if self.check_list(self.gameboard[move[0],:move[1] + 1],move[1],self.rep[self.turn]):
            self.gameboard[move[0],np.argwhere(self.gameboard[move[0],:move[1] + 1] == self.rep[self.turn])[-1,0]:move[1]] = self.rep[self.turn]
        if self.check_list(self.gameboard[move[0],move[1]:],0,self.rep[self.turn]):
            self.gameboard[move[0],move[1] + 1:np.argwhere(self.gameboard[move[0],move[1]:] == self.rep[self.turn])[0,0] + move[1]] = self.rep[self.turn]
        
        # checks if the rightways diagonal containing move played has a valid othello moves and flips opponents pieces accordingly 
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
        
        # checks if the leftways diagonal containing move played has a valid othello moves and flips opponents pieces accordingly 
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
    
    # returns a list of possible moves 
    def possible_moves(self):
        if np.argwhere(self.gameboard == 0).size != 0:
            return np.argwhere(self.gameboard==0)[self.has_moves(np.argwhere(self.gameboard==0)[:,0],np.argwhere(self.gameboard==0)[:,1],self.rep[self.turn])]
        else:
            return np.array([])

    # does event handling on game screen
    def checkpress(self,click):
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):

                if (self.boardrects[i][j]).collidepoint(click.pos) and self.gameboard[i][j]==0 and self.valid_move(i,j,self.rep[self.turn]):
                    self.make_move((i,j))
                    if self.check_win_condition((i,j)):
                        return self.check_win_condition((i,j))
                    self.switch_turn()
                    # if current player has no valid moves switch turn
                    if not self.has_moves(np.argwhere(self.gameboard == 0).T[[0]],np.argwhere(self.gameboard == 0).T[[1]],self.rep[self.turn]).any():
                        self.switch_turn()


    def check_win_condition(self,move):

        # if board is full check number of pieces
        if np.argwhere(self.gameboard == 0).size == 0:
            if np.argwhere(self.gameboard == 1).size == np.argwhere(self.gameboard == 2).size:
                self.winner = -1
                return -1
            elif np.argwhere(self.gameboard == 1).size > np.argwhere(self.gameboard == 2).size:
                self.winner = 1
                return 1
            else:
                self.winner = 2
                return 2


        else:
            # if board is not full check if valid moves are left for either player
            if not self.has_moves(np.argwhere(self.gameboard == 0).T[[0]],np.argwhere(self.gameboard == 0).T[[1]],1).any() and not self.has_moves(np.argwhere(self.gameboard == 0).T[[0]],np.argwhere(self.gameboard == 0).T[[1]],2).any():
                if np.argwhere(self.gameboard == 1).size == np.argwhere(self.gameboard == 2).size:
                    self.winner = -1
                    return -1
                elif np.argwhere(self.gameboard == 1).size > np.argwhere(self.gameboard == 2).size:
                    self.winner = 1
                    return 1
                else :
                    self.winner = 2
                    return 2
            else:
                return 0 # if valid moves are left for either player
