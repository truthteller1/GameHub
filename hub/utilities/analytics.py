import pygame
import os
from .button import *
import csv
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.gridspec import GridSpec

hub = Path(__file__).parent.parent
button = hub.parent / "Graphics" / "theme_designs"

class Analytics:
    def __init__(self,SW,SH,screen):
        self.screen = screen
        self.SW = SW
        self.SH = SH
        self.analytics_quit = Button((SW/2,SH/2+230),screen,img = button / "backbutton.png",size=(340,90))
        self.analytics_quit.assigntext("DONE",30,None,(241,95,95))
        self.analytics_show = Button((SW/2,SH/2 + 135),self.screen,img = button / "regularbutton.png",size=(440,90))
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
                self.analytics_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-80),screen,img=button / "leftbutton.png",size=(65,69),sqrscaling=True))
            else:
                self.analytics_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-80),screen,img=button / "rightbutton.png",size=(65,69),sqrscaling=True))


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
                player_totalgames = {}
                csvreader = csv.reader(file)
                for row in csvreader:
                    game_stats[row[1]]+=1
                    if row[0] == "Win":
                        if row[2] in player_wins.keys():
                            player_wins[row[2]] +=1

                        else:
                            player_wins[row[2]] = 1

                        if not(row[3] in player_wins.keys()):
                            player_wins[row[3]] = 0

                    player_totalgames[row[2]] = player_totalgames.get(row[2],0) + 1
                    player_totalgames[row[3]] = player_totalgames.get(row[3],0) + 1

                sorted_wins = dict(sorted(player_wins.items(), key=lambda item: item[1],reverse=True))
                sorted_by_winrate = dict(sorted(player_wins.items(), key=lambda item: item[1]/player_totalgames[item[0]],reverse=True))
                winrate = [sorted_by_winrate[key]/player_totalgames[key] for key in sorted_by_winrate]

                fig = plt.figure(figsize=(10, 8))
                gs = GridSpec(2, 2, figure=fig)

                #Graph of win rate per player, for top 10 players by win rate
                ax1 = fig.add_subplot(gs[0, :])
                ax1.bar(list(sorted_by_winrate.keys())[:10],winrate[:10])
                ax1.set_title("Win rate of top 10 players")
                plt.xticks(rotation=45)

                # Pie chart of games played
                if any(game_stats.values()):
                    label = ["TicTacToe","Othello","Connect4","Chain Reaction","Checkers"]
                    ax2 = fig.add_subplot(gs[1, 0])
                    ax2.pie(list(game_stats.values()),labels = label)
                    ax2.set_title("Most played games")

                # Wins per player, for the top 5 players by total wins
                ax3 = fig.add_subplot(gs[1, 1])
                ax3.bar(list(sorted_wins.keys())[:5],list(sorted_wins.values())[:5])
                ax3.set_title("Wins of top 5 players")
                plt.xticks(rotation=45)

                plt.tight_layout()
                plt.show()

        elif self.analytics_quit.rect.collidepoint(event.pos):
            return True
