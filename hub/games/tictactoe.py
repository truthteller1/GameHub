from .game_class import Game
import pygame

class TicTacToe(Game):
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
                if self.gameboard[i][j] == 1:
                    #REPLACE THIS WITH X
                    pygame.draw.circle(self.screen,(255,0,0),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side/2),side//2)
                elif self.gameboard[i][j] == 2:
                    #REPLACE WITH O
                    pygame.draw.circle(self.screen,(0,0,255),(bx + j*(buffer+side)+side//2,by+i*(buffer+side)+side//2),side//2)
    
    def checkpress(self,click):
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if (self.boardrects[i][j]).collidepoint(click.pos) and self.gameboard[i][j]==0:
                    self.make_move((i,j))
                    self.check_win_condition()
                    self.switch_turn()
    def check_win_condition(self):
        return 