from .game_class import Game
import pygame

class Othello(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        self.screen = screen
        self.boardrects = []
        #restructure vars
        bx = 20
        by = 20
        buffer  = 10
        side = 30
        self.gameboard[3][3]=1
        self.gameboard[4][4]=1
        self.gameboard[4][3]=2
        self.gameboard[3][4]=2
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
                pygame.draw.rect(self.screen, (0,180,0), self.boardrects[i][j])
                if self.gameboard[i][j] == 1:
                    pygame.draw.circle(self.screen,(0,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2)
                elif self.gameboard[i][j] == 2:
                    pygame.draw.circle(self.screen,(255,255,255),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2)
    
    def check_validity(self,i,j):
        if self.turn == self.p1:
            t = 1
        else:
            t=2
        validdir = [] # down, up, right, left, \ down,
        points = []
        p=i+1
        w = True
        while p<8:
            w=False
            if self.gameboard[p][j] == 0 or (self.gameboard[p][j]==t and p==i+1):
                validdir.append(False)
                points.append(None)
                break
            elif self.gameboard[p][j]==t and p!=i+1:
                validdir.append(True)
                points.append((p,j))
                break
            p+=1
        else:
            validdir.append(False)
        if w:
            validdir.append(False)
        p=i-1
        w=True
        while p>=0:
            w=False
            if self.gameboard[p][j] == 0 or (self.gameboard[p][j]==t and p==i-1):
                validdir.append(False)
                points.append(None)
                break
            elif self.gameboard[p][j]==t and p!=i-1:
                validdir.append(True)
                points.append((p,j))
                break
            p-=1
        else:
            validdir.append(False)
        if w:
            validdir.append(False)
        p=j+1
        w=True
        while p<8:
            w=False
            if self.gameboard[i][p] == 0 or (self.gameboard[i][p]==t and p==j+1):
                validdir.append(False)
                points.append(None)
                break
            elif self.gameboard[i][p]==t and p!=j+1:
                validdir.append(True)
                points.append((i,p))
                break
            p+=1
        else:
            validdir.append(False)
        if w:
            validdir.append(False)
        p=j-1
        w=True
        while p>=0:
            w=False
            if self.gameboard[i][p] == 0 or (self.gameboard[i][p]==t and p==j-1):
                validdir.append(False)
                points.append(None)
                break
            elif self.gameboard[i][p]==t and p!=j-1:
                validdir.append(True)
                points.append((i,p))
                break
            p-=1
        else:
            validdir.append(False)
        if w:
            validdir.append(False)
        p=i+1
        q=j+1
        w=True
        while p<8 and q<8:
            w=False
            if self.gameboard[p][q] == 0 or (self.gameboard[p][q]==t and p==i+1):
                validdir.append(False)
                points.append(None)
                break
            elif self.gameboard[p][q]==t and p!=i+1:
                validdir.append(True)
                points.append((p,q))
                break
            p+=1
            q+=1
        else:
            validdir.append(False)
        if w:
            validdir.append(False)
        p=i+1
        q=j-1
        w=True
        while p<8 and q>=0:
            w=False
            if self.gameboard[p][q] == 0 or (self.gameboard[p][q]==t and p==i+1):
                validdir.append(False)
                points.append(None)
                break
            elif self.gameboard[p][q]==t and p!=i+1:
                validdir.append(True)
                points.append((p,q))
                break
            p+=1
            q-=1
        else:
            validdir.append(False)
        if w:
            validdir.append(False)
        p=i-1
        q=j+1
        w=True
        while p>=0 and q<8:
            w=False
            if self.gameboard[p][q] == 0 or (self.gameboard[p][q]==t and q==j+1):
                validdir.append(False)
                points.append(None)
                break
            elif self.gameboard[p][q]==t and q!=j+1:
                validdir.append(True)
                points.append((p,q))
                break
            p-=1
            q+=1
        else:
            validdir.append(False)
        if w:
            validdir.append(False)
        p=i-1
        q=j-1
        w=True
        while p>=0 and q>=0:
            w=False
            if self.gameboard[p][q] == 0 or (self.gameboard[p][q]==t and p==i-1):
                validdir.append(False)
                points.append(None)
                break
            elif self.gameboard[p][q]==t and p!=i-1:
                validdir.append(True)
                points.append((p,q))
                break
            p-=1
            q-=1
        else:
            validdir.append(False)
        if w:
            validdir.append(False)
        print(validdir)
        return validdir,points

    def make_move(self, move,validdir,points):
        i,j=move
        print(move)
        if self.turn == self.p1:
            t = 1
        else:
            t=2
        k = 0
        p=i+1
        if validdir[k]:
            while p<8:
                if self.gameboard[p][j]==t:
                    break
                self.gameboard[p][j] = t
                p+=1
        p=i-1
        k+=1
        if validdir[k]:
            while p>=0:
                if self.gameboard[p][j]==t:
                    break
                self.gameboard[p][j] = t
                p-=1
        p=j+1
        k+=1
        if validdir[k]:
            while p<8:
                if self.gameboard[i][p]==t:
                    break
                self.gameboard[i][p] = t
                p+=1
        p=j-1
        k+=1
        if validdir[k]:
            while p<8:
                if self.gameboard[i][p]==t:
                    break
                self.gameboard[i][p] = t
                p-=1
        p=i+1
        q=j+1
        k+=1
        if validdir[k]:
            while p<8 and q<8:
                if self.gameboard[p][q]==t:
                    break
                self.gameboard[p][q] = t
                p+=1
                q+=1
        p=i+1
        q=j-1
        k+=1
        if validdir[k]:
            while p<8 and q>=0:
                if self.gameboard[p][q]==t:
                    break
                self.gameboard[p][q] = t
                p+=1
                q-=1
        p=i-1
        q=j+1
        k+=1
        if validdir[k]:
            while p>=0 and q<8:
                if self.gameboard[p][q]==t:
                    break
                self.gameboard[p][q] = t
                p-=1
                q+=1
        p=i-1
        q=j-1
        k+=1
        if validdir[k]:
            while p>=0 and q>=0:
                if self.gameboard[p][q]==t:
                    break
                self.gameboard[p][q] = t
                p-=1
                q-=1
        super().make_move(move)

    def checkpress(self,click):
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if (self.boardrects[i][j]).collidepoint(click.pos) and self.gameboard[i][j]==0:
                    validdir,points = self.check_validity(i,j)
                    if True in validdir:
                        self.make_move((i,j),validdir,points)
                        self.check_win_condition()
                        self.switch_turn()