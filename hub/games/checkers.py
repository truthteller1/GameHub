from .game_class import Game
from .avatar_render import *
import pygame
import numpy as np
from .text import Text

class Checkers(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        self.screen = screen
        self.boardrects = []
        self.selected = None
        self.has_moves = np.vectorize(self.check_existence)
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if i<=2 and (i+j)%2!=0:
                    self.gameboard[i][j] = 1
                if i>=(self.gameboard.shape[0]-1-2) and (i+j)%2!=0:
                    self.gameboard[i][j] = 2
        
        #restructure vars
        bx = 500-240
        by = 160
        buffer  = 0
        side = 60
        self.background = pygame.transform.smoothscale(pygame.image.load("../Graphics/sharprect.png"),((60*self.gameboard.shape[0]+8)*968//800,(60*self.gameboard.shape[1]+8)*968//800))
        self.bgrect = self.background.get_rect()
        self.bgrect.center = (bx+60*4,by+60*4)
        self.avim = pygame.transform.smoothscale(pygame.image.load("../Graphics/roundrect.png"),(180*968//800,320*968//800))
        self.avrect1 = pygame.Rect(0,0,180*968//800,320*968//800)
        self.avrect1.midtop = (130,180)
        self.avrect2 = pygame.Rect(0,0,180*968//800,320*968//800)
        self.avrect2.midtop = (1000-130,180)
        self.text1 = Text(self.p1,20,(130,500),screen,color=(189,255,209))
        self.text2 = Text(self.p2,20,(1000-130,500),screen,color=(189,255,209))
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))

        self.avatars = {self.p1:parse_avatar(p1),self.p2: parse_avatar(p2)}

        
    #for rendering gameboard and pieces
    def renderboard(self, dimensions):
        bx = 500-240
        by = 160
        buffer  = 0
        side = 60
        self.screen.blit(self.background,self.bgrect)
        for i in range(self.gameboard.shape[0]):
            #self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                #self.boardrects[i].append(pygame.Rect((bx + j*(buffer+side),by+i*(buffer+side),side,side)))
                if (i+j)%2==0:    
                    pygame.draw.rect(self.screen, (0,150,0), self.boardrects[i][j])
                if abs(self.gameboard[i][j]) == 1:
                    #REPLACE THIS WITH X
                    if self.selected == (i,j):
                        pygame.draw.circle(self.screen,(100,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2-5)
                    else:
                        pygame.draw.circle(self.screen,(255,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2-5)
                elif abs(self.gameboard[i][j]) == 2:
                    #REPLACE WITH O
                    if self.selected == (i,j):
                        pygame.draw.circle(self.screen,(0,0,100),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2-5)
                    else:
                        pygame.draw.circle(self.screen,(0,0,255),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2-5)
                if self.gameboard[i][j]<0:
                    pygame.draw.circle(self.screen, (255,165,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),5)
        self.screen.blit(self.avim,self.avrect1)
        self.screen.blit(self.avim,self.avrect2)
        self.text1.render(scale = 1+ 0.1*(self.rep[self.turn]%2))
        self.text2.render(scale = 1+ 0.1*(self.rep[self.turn]//2))
        self.renderav((130,300),self.p1)
        pygame.draw.circle(self.screen,(255,0,0),(130,250),15)
        self.renderav((1000-130,300),self.p2)
        pygame.draw.circle(self.screen,(0,0,255),(1000-130,250),15)

    #checks existence of move for a coin on the board given its position as arguments: i,j are its indices in self.gameboard
    def check_existence(self,i,j): #move is position of coin
        move = (i,j)
        if (move[1]+move[0])%2==0:
            return False
        rdiag = self.gameboard.diagonal(move[1]-move[0])
        rind = min(move[0],move[1])
        ldiag = self.gameboard[:,::-1].diagonal(self.gameboard.shape[1]-1-move[1]-move[0])
        lind = min(move[0],self.gameboard.shape[1]-1-move[1])

        if self.gameboard[move]>0:
            if self.turn == self.p1:
                #checking normal forward moves
                if (len(rdiag)>=rind+2 and (rdiag[rind+1])==0) or (len(ldiag)>=lind+2 and ldiag[lind+1] == 0):
                    return True
                #checking jumping moves
                if (len(rdiag)>=rind+3 and abs(rdiag[rind+1])==2 and rdiag[rind+2]==0) or (len(ldiag)>=lind+3 and abs(ldiag[lind+1])==2 and ldiag[lind+2]==0):
                    return True
                else:
                    return False
            else:
                #checking normal forward moves
                if (rind>=1 and rdiag[rind-1]==0) or (lind>=1 and ldiag[lind-1]==0):
                    return True
                #checking jumping moves
                if (rind>=2 and abs(rdiag[rind-1])==1 and rdiag[rind-2]==0) or (lind>=2 and abs(ldiag[lind-1])==1 and ldiag[lind-2]==0):
                    return True
                else:
                    return False
        
        #if no coin present,return false - no move exists
        elif self.gameboard[move]==0:
            return False
        
        #checks move validity for kings in all 4 possible directions: when self.gameboard[i][j] < 0
        else:
            other = self.rep[self.turn]%2 +1
            if (rind>=1 and rdiag[rind-1]==0) or (lind>=1 and ldiag[lind-1]==0) or (len(rdiag)>=rind+2 and rdiag[rind+1]==0) or (len(ldiag)>=lind+2 and ldiag[lind+1] == 0) or (len(rdiag)>=rind+3 and abs(rdiag[rind+1])==other and rdiag[rind+2]==0) or (len(ldiag)>=lind+3 and abs(ldiag[lind+1])==other and ldiag[lind+2]==0) or (rind>=2 and abs(rdiag[rind-1])==other and rdiag[rind-2]==0) or (lind>=2 and abs(ldiag[lind-1])==other and ldiag[lind-2]==0):
                return True
            else:
                return False

    #implementation of jumping by board pieces, checks for available jumps, when available makes jump and recursively calls itself
    #when no jump exists, returns false and ends recursion
    def jump(self, pos):
        self.selected = None
        rdiag = self.gameboard.diagonal(pos[1]-pos[0])
        rind = min(pos[0],pos[1])
        ldiag = self.gameboard[:,::-1].diagonal(self.gameboard.shape[1]-1-pos[1]-pos[0])
        lind = min(pos[0],self.gameboard.shape[1]-1-pos[1])
        coin = self.rep[self.turn]
        other = self.rep[self.turn]%2 +1

        #checking one direction
        if (len(rdiag)>=rind+3 and abs(rdiag[rind+1])==other and rdiag[rind+2]==0) and (self.turn == self.p1 or self.gameboard[pos]<0):
            self.gameboard[pos[0]+1][pos[1]+1]=0
            if pos[0]+2 == self.gameboard.shape[0]-1 or self.gameboard[pos]<0:
                self.gameboard[pos[0]+2][pos[1]+2] = -coin
            else:
                self.gameboard[pos[0]+2][pos[1]+2] = coin
            self.gameboard[pos] = 0
            self.jump((pos[0]+2,pos[1]+2))

        #checking
        elif (len(ldiag)>=lind+3 and abs(ldiag[lind+1])==other and ldiag[lind+2]==0) and (self.turn == self.p1 or self.gameboard[pos]<0):
            
            self.gameboard[pos[0]+1][pos[1]-1]=0
            if pos[0]+2 == self.gameboard.shape[0]-1 or self.gameboard[pos]<0:
                self.gameboard[pos[0]+2][pos[1]-2] = -coin
            else:
                self.gameboard[pos[0]+2][pos[1]-2] = coin
            self.gameboard[pos] = 0
            self.jump((pos[0]+2,pos[1]-2))

        #checking
        elif (rind>=2 and abs(rdiag[rind-1])==other and rdiag[rind-2]==0) and (self.turn == self.p2 or self.gameboard[pos]<0):
            self.gameboard[pos[0]-1][pos[1]-1]=0
            if pos[0]-2 == 0 or self.gameboard[pos]<0:
                self.gameboard[pos[0]-2][pos[1]-2] = -coin
            else:
                self.gameboard[pos[0]-2][pos[1]-2] = coin
            self.gameboard[pos] = 0
            self.jump((pos[0]-2,pos[1]-2))

        #checking
        elif (lind>=2 and abs(ldiag[lind-1])==other and ldiag[lind-2]==0) and (self.turn == self.p2 or self.gameboard[pos]<0):
            self.gameboard[pos[0]-1][pos[1]+1]=0
            if pos[0]-2 == 0 or self.gameboard[pos]<0:
                self.gameboard[pos[0]-2][pos[1]+2] = -coin
            else:
                self.gameboard[pos[0]-2][pos[1]+2] = coin
            self.gameboard[pos] = 0
            self.jump((pos[0]-2,pos[1]+2))
        
        #returning False when jump does not exist
        else:
            return False

    
    def make_move(self, move):
        if (move[1]+move[0])%2==0:
            return False
        print(self.gameboard)
        rdiag = self.gameboard.diagonal(self.selected[1]-self.selected[0])
        rind = min(self.selected[0],self.selected[1])
        ldiag = self.gameboard[:,::-1].diagonal(self.gameboard.shape[1]-1-self.selected[1]-self.selected[0])
        lind = min(self.selected[0],self.gameboard.shape[1]-1-self.selected[1])

        #making moves for normal(non-jump) moves
        if self.turn == self.p1:
            print(move==(self.selected[0]+1,self.selected[1]+1),self.gameboard[move]==0)
            if (move==(self.selected[0]+1,self.selected[1]-1) or move==(self.selected[0]+1,self.selected[1]+1)) and self.gameboard[move]==0:
                if move[0] == self.gameboard.shape[0]-1 or self.gameboard[self.selected]==-1:
                    self.gameboard[self.selected]=0
                    self.gameboard[move] = -1
                else:
                    self.gameboard[self.selected]=0
                    self.gameboard[move] = 1
                return True
            if self.gameboard[self.selected]==-1:
                if (move==(self.selected[0]-1,self.selected[1]-1) or move==(self.selected[0]-1,self.selected[1]+1)) and self.gameboard[move]==0:
                    self.gameboard[self.selected]=0
                    self.gameboard[move] = -1
                    return True
            
        else:
            print(move==(self.selected[0]+1,self.selected[1]+1),self.gameboard[move]==0)
            if (move==(self.selected[0]-1,self.selected[1]-1) or move==(self.selected[0]-1,self.selected[1]+1)) and self.gameboard[move]==0:
                if move[0] == 0 or self.gameboard[self.selected]==-2:
                    self.gameboard[self.selected]=0
                    self.gameboard[move] = -2
                else:
                    self.gameboard[self.selected]=0
                    self.gameboard[move] = 2
                return True
            if self.gameboard[self.selected]==-2:
                if (move==(self.selected[0]+1,self.selected[1]-1) or move==(self.selected[0]+1,self.selected[1]+1)) and self.gameboard[move]==0:
                    self.gameboard[self.selected]=0
                    self.gameboard[move] = -2
                    return True
                
        coin = self.rep[self.turn]
        other = self.rep[self.turn]%2 +1
        pos = self.selected #SOMEONE CHANGE THIS PLEASE ToT
        #making moves for jumps
        if (len(rdiag)>=rind+3 and abs(rdiag[rind+1])==other and rdiag[rind+2]==0) and (self.turn == self.p1 or self.gameboard[pos]<0) and move==(pos[0]+2,pos[1]+2):
            self.gameboard[pos[0]+1][pos[1]+1]=0
            if pos[0]+2 == self.gameboard.shape[0]-1 or self.gameboard[pos]<0:
                self.gameboard[pos[0]+2][pos[1]+2] = -coin
            else:
                self.gameboard[pos[0]+2][pos[1]+2] = coin
            self.gameboard[pos] = 0
            self.jump((pos[0]+2,pos[1]+2))
            return True

        elif (len(ldiag)>=lind+3 and abs(ldiag[lind+1])==other and ldiag[lind+2]==0) and (self.turn == self.p1 or self.gameboard[pos]<0)and move==(pos[0]+2,pos[1]-2):
            self.gameboard[pos[0]+1][pos[1]-1]=0
            if pos[0]+2 == self.gameboard.shape[0]-1 or self.gameboard[pos]<0:
                self.gameboard[pos[0]+2][pos[1]-2] = -coin
            else:
                self.gameboard[pos[0]+2][pos[1]-2] = coin
            self.gameboard[pos] = 0
            self.jump((pos[0]+2,pos[1]-2))
            return True

        elif (rind>=2 and abs(rdiag[rind-1])==other and rdiag[rind-2]==0) and (self.turn == self.p2 or self.gameboard[pos]<0)and move==(pos[0]-2,pos[1]-2):
            self.gameboard[pos[0]-1][pos[1]-1]=0
            if pos[0]-2 == 0 or self.gameboard[pos]<0:
                self.gameboard[pos[0]-2][pos[1]-2] = -coin
            else:
                self.gameboard[pos[0]-2][pos[1]-2] = coin
            self.gameboard[pos] = 0
            self.jump((pos[0]-2,pos[1]-2))
            return True

        elif (lind>=2 and abs(ldiag[lind-1])==other and ldiag[lind-2]==0) and (self.turn == self.p2 or self.gameboard[pos]<0)and move==(pos[0]-2,pos[1]+2):
            self.gameboard[pos[0]-1][pos[1]+1]=0
            if pos[0]-2 == 0 or self.gameboard[pos]<0:
                self.gameboard[pos[0]-2][pos[1]+2] = -coin
            else:
                self.gameboard[pos[0]-2][pos[1]+2] = coin
            self.gameboard[pos] = 0
            self.jump((pos[0]-2,pos[1]+2))
            return True
        print(lind>=2, abs(ldiag[lind-1])==other, ldiag[lind-2]==0)
        
    
    #processes clicks on the board, makes moves accordingly if corresponding click is valid
    def checkpress(self,click):
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if (self.boardrects[i][j]).collidepoint(click.pos):
                    print((i,j), self.selected, self.check_existence(i,j),self.rep[self.turn]==abs(self.gameboard[i][j]))
                    if self.selected!=(i,j):
                        if self.check_existence(i,j) and self.rep[self.turn]==abs(self.gameboard[i][j]):
                            self.selected = (i,j)
                    if self.selected:
                        # if self.selected == (i,j):
                        #     self.selected = None
                        # else:
                            if self.make_move((i,j)):
                                self.switch_turn()
                                if self.check_win_condition():
                                    return self.check_win_condition()
                                
    #checks win condition using numpy, returns 1 or 2 corresponding to the game winner
    def check_win_condition(self):
        arr = np.argwhere(abs(self.gameboard)==self.rep[self.turn])
        if arr.shape[0]==0 or (not (self.has_moves(arr[:,0],arr[:,1])).any()): # checks if player has no moves or if player is out of coins
            self.winner = 3 - self.rep[self.turn]
            return 3 - self.rep[self.turn]
