from .game_class import Game
from pathlib import Path
from .avatar_render import *
import pygame
import numpy as np
from .text import Text

img_dir = Path(__file__).parent.parent.parent / "Graphics" / "chain_rxn" 
button = img_dir.parent / "theme_designs"

class Chain_rxn(Game):
    def __init__(self, p1, p2, starter, board, screen):
        super().__init__(p1,p2,starter,board)
        self.board = self.gameboard
        self.screen = screen
        self.boardrects = []
        self.size = self.screen.get_size()
        self.avatars = {self.p1:parse_avatar(p1),self.p2: parse_avatar(p2)}
        
        # parameters for board size and individual square size
        self.buffer = buffer = 10
        self.side = side = 80
        self.bx = bx = (self.size[0] - self.gameboard.shape[0] * self.side - (self.gameboard.shape[0] - 1) * self.buffer) // 2
        self.by = by = (self.size[1] - self.gameboard.shape[1] * self.side - (self.gameboard.shape[1] - 1) * self.buffer) // 2
        self.atoms = [[],[]]

        # seting values for variables required for rendering avatars
        self.background = pygame.transform.smoothscale(pygame.image.load(button / "sharprect.png"),((90*self.gameboard.shape[0]+5)*968//800,(90*self.gameboard.shape[1]+5)*968//800))
        self.bgrect = self.background.get_rect()
        self.bgrect.center = (500,400)
        self.avim = pygame.transform.smoothscale(pygame.image.load(button / "roundrect.png"),(180*968//800,320*968//800))
        self.avrect1 = pygame.Rect(0,0,180*968//800,320*968//800)
        self.avrect1.midtop = (130,180)
        self.avrect2 = pygame.Rect(0,0,180*968//800,320*968//800)
        self.avrect2.midtop = (1000-130,180)
        self.text1 = Text(self.p1,20,(130,500),screen,color=(189,255,209))
        self.text2 = Text(self.p2,20,(1000-130,500),screen,color=(189,255,209))

        # setting up rects at each square on the gameboard
        for i in range(2):
            for j in range(3):
                img_path = img_dir / f"atom{i+1},{j+1}.png"
                self.atoms[i].append(pygame.image.load(img_path).convert_alpha())
                self.atoms[i][j] = pygame.transform.scale(self.atoms[i][j],(self.side,self.side))
        for i in range(self.gameboard.shape[0]):
            self.boardrects.append([])
            for j in range(self.gameboard.shape[1]):
                self.boardrects[i].append(pygame.Rect((self.bx + j*(self.buffer+self.side),self.by+i*(self.buffer+self.side),self.side,self.side)))

    # for rendering gameboard
    def renderboard(self, dimensions):
        buffer  = 10
        side = 80
        bx = (self.size[0] - self.gameboard.shape[0] * side - (self.gameboard.shape[0] - 1) * buffer) // 2
        by = (self.size[1] - self.gameboard.shape[1] * side - (self.gameboard.shape[1] - 1) * buffer) // 2
        
        # renders and background each square (rect) of the gameboard
        self.screen.blit(self.background,self.bgrect)
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                
                pygame.draw.rect(self.screen, (0,150,0), self.boardrects[i][j])
                if self.gameboard[i][j][0] != 0:
                    self.screen.blit(self.atoms[self.gameboard[i,j,0] - 1][self.gameboard[i,j,1] - 1],(bx + j*(buffer+side),by+i*(buffer+side)))
        
        # rendering avatars of both players
        Text("Your turn!",60,(500 + ((-1)**(self.rep[self.turn]))*375,180),self.screen,color=(189,255,209)).render() 
        self.screen.blit(self.avim,self.avrect1)
        self.screen.blit(self.avim,self.avrect2)
        self.text1.render(scale = 1.2+ 0.1*(self.rep[self.turn]%2))
        self.text2.render(scale = 1.2+ 0.1*(self.rep[self.turn]//2))
        self.renderav((125,330),self.p1)
        self.screen.blit(self.atoms[0][0],(self.size[0] // 8 - self.side // 2,225))
        self.renderav((1000-125,330),self.p2)
        self.screen.blit(self.atoms[1][0],(self.size[0] * 7 // 8 - self.side // 2, 225))


    def make_move(self, move):
        if self.gameboard[move][1] == 0:
            self.gameboard[move] = [self.rep[self.turn],1] # if unoccupied place one atom

        elif (move == (0,0) or move == (self.gameboard.shape[0] - 1,0) or move == (0, self.gameboard.shape[1] - 1) or move == (self.gameboard.shape[0] - 1, self.gameboard.shape[1] - 1)) and self.gameboard[move][1] == 1:
            
            self.gameboard[move] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    # if corner has 2 atoms at this instant split in one atom to each neighbouring square
                    if move[0] + i >=0 and move[0] + i < self.gameboard.shape[0] and move[1] + j >= 0 and move[1] + j < self.gameboard.shape[1] and (i != 0 or j != 0) and (i == 0 or j == 0):
                        self.gameboard[move[0] + i, move[1] + j, 0] = self.rep[self.turn]
                        self.make_move((move[0] + i, move[1] + j))
                        if self.check_win_condition():
                            return

        elif move[0] * move[1] * (move[0] - self.gameboard.shape[0] + 1) * (move[1] - self.gameboard.shape[1] + 1) == 0 and self.gameboard[move][1] == 2:
            
            self.gameboard[move] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    # if edge has 3 atoms at this instant split into one atom to each neighbouring square
                    if move[0] + i >=0 and move[0] + i < self.gameboard.shape[0] and move[1] + j >= 0 and move[1] + j < self.gameboard.shape[1] and (i != 0 or j != 0) and (i == 0 or j == 0):
                        self.gameboard[move[0] + i, move[1] + j, 0] = self.rep[self.turn]
                        self.make_move((move[0] + i, move[1] + j))
                        if self.check_win_condition():
                            return
                        
        elif self.gameboard[move][1] == 3:
            
            self.gameboard[move] = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    # if central square has 4 atoms at this instant split into one atom each into neighbouring squares
                    if move[0] + i >=0 and move[0] + i < self.gameboard.shape[0] and move[1] + j >= 0 and move[1] + j < self.gameboard.shape[1] and (i != 0 or j != 0) and (i == 0 or j == 0):
                        self.gameboard[move[0] + i, move[1] + j, 0] = self.rep[self.turn]
                        self.make_move((move[0] + i, move[1] + j))
                        if self.check_win_condition():
                            return

        else:
            self.gameboard[move][1] += 1 # if already occupied with same colour add another atom(given it doesnt exceed limit)

    # for event handling in game screen
    def checkpress(self,click):

        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                # play move even if square is occupied as long as colour of occupying atom is same as player)
                if ((self.boardrects[i][j]).collidepoint(click.pos)) and ((self.gameboard[i][j][0] == self.rep[self.turn] or self.gameboard[i,j,0] == 0)):
                    self.make_move((i,j))
                    if self.check_win_condition():
                        return self.check_win_condition()
                    self.switch_turn()
                    

    def check_win_condition(self):
        # checks if opponents colour is still present on the board and it isnt the first move of the game
        if np.argwhere(self.gameboard[:,:,0] == self.rep[self.turn]).size != 2 and np.argwhere(self.gameboard[:,:,0] == 3 - self.rep[self.turn]).size == 0:
            self.winner = self.rep[self.turn]
            return self.rep[self.turn]
        else:
            return 0
