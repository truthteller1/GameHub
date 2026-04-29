import pygame
import os
from .button import *
import csv
import matplotlib.pyplot as plt

class Analytics:
    def __init__(self,SW,SH,screen):
        self.screen = screen
        self.SW = SW
        self.SH = SH
        self.analytics_quit = Button((SW/2,SH/2+230),screen,img = "../Graphics/backbutton.png",size=(340,90))
        self.analytics_quit.assigntext("DONE",30,None,(241,95,95))
        self.analytics_show = Button((SW/2,SH/2 + 150),self.screen,img = "../Graphics/regularbutton.png",size=(440,90))
        self.analytics_show.assigntext("SHOW",30,None)
        self.analytics_buttons = []
        self.analytics_iter = 0
        # for i in range(2):
        #     self.analytics_buttons.append(Button((self.SW/2-((-1)**i)*200,self.SH/2-80),self.screen,color=(8,69,4),border_width=0,size=(40,90)))
        #     if i % 2 == 0:
        #         self.analytics_buttons[-1].assigntext("<",30,None)
        #     else:
        #         self.analytics_buttons[-1].assigntext(">",30,None)
        for i in range(2):
            if i % 2 == 0:
                self.analytics_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-80),screen,img="../Graphics/leftbutton.png",size=(65,69),sqrscaling=True))
            else:
                self.analytics_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-80),screen,img="../Graphics/rightbutton.png",size=(65,69),sqrscaling=True))

        '''
                        with open("history.csv","r",newline='') as file:
                            game_stats = {"tictactoe":0,"othello":0,"connect4":0,"chain_rxn":0,"checkers":0}
                            player_wins = {}
                            csvreader = csv.reader(file)
                            for row in csvreader:
                                game_stats[row[1]]+=1
                                if row[0] == "win":
                                    if row[2] in player_wins.keys():
                                        player_wins[row[2]] +=1
                                    else:
                                        player_wins[row[2]] = 1
                                    if not(row[3] in player_wins.keys()):
                                        player_wins[row[3]] = 0
                            plt.subplot(121)
                            plt.bar(list(player_wins.values()),list(player_wins.keys()))
                            plt.title("Wins")
                            plt.subplot(122)
                            plt.pie(list(game_stats.values()),labels = list(game_stats.keys()))
                            plt.title("gamesplayed")
                            plt.show()'''

    def interact(self,event):
        if self.analytics_buttons[0].rect.collidepoint(event.pos):
            self.analytics_iter = (self.analytics_iter - 1) % 5
        elif self.analytics_buttons[1].rect.collidepoint(event.pos):
            self.analytics_iter = (self.analytics_iter + 1) % 5
        elif self.analytics_show.rect.collidepoint(event.pos):
            os.system(f"bash leaderboard.sh {self.analytics_iter + 1}")
            with open("history.csv","r",newline='') as file:
                            game_stats = {"tictactoe":0,"othello":0,"connect4":0,"chain_rxn":0,"checkers":0}
                            player_wins = {}
                            csvreader = csv.reader(file)
                            for row in csvreader:
                                game_stats[row[1]]+=1
                                if row[0] == "win":
                                    if row[2] in player_wins.keys():
                                        player_wins[row[2]] +=1
                                    else:
                                        player_wins[row[2]] = 1
                                    if not(row[3] in player_wins.keys()):
                                        player_wins[row[3]] = 0
                            plt.subplot(121)
                            plt.bar(list(player_wins.values()),list(player_wins.keys()))
                            plt.title("Wins")
                            plt.subplot(122)
                            plt.pie(list(game_stats.values()),labels = list(game_stats.keys()))
                            plt.title("gamesplayed")
                            plt.show()
        elif self.analytics_quit.rect.collidepoint(event.pos):
            return True
