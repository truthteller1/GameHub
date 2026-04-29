import numpy as np
from .avatar_render import *

class Game:
    def __init__(self, p1, p2, starter, board):
        self.p1 = p1
        self.p2 = p2
        self.rep = {p1:1, p2:2, 1:p1, 2:p2}
        self.turn = starter
        self.gameboard = np.zeros(board, dtype=int)
        self.winner = False

    def switch_turn(self):
        self.turn = self.rep[ 3 - self.rep[self.turn]] #self.p1 if (self.turn == self.p2) else self.p2

    def make_move(self, move):
        if (self.turn == self.p1):
            self.gameboard[move] = 1
        else:
            self.gameboard[move]  = 2
        
    def check_win_condition(self):
        pass

    def renderav(self, pos, player):
        if self.turn != player:
            transparency = 180
        else:
            transparency = 255
        avatar_render(self.avatars[player],pos,self.screen,transparency,0.4)
