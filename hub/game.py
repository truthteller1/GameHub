import pygame
import sys
import time
from games.tictactoe import TicTacToe
from games.connect4 import Connect4
from games.othello import Othello
from games.chain_rxn import Chain_rxn
from games.checkers import Checkers
from games.avatar_render import *
import matplotlib.pyplot as plt
import csv
import random
import os

white = (255,255,255)
black = (0,0,0)
navy = (1,3,43)
red = (255, 0,0)
orange = (255,165,0)

player1 = sys.argv[1]
player2 = sys.argv[2]


pygame.init()
pygame.mixer.init()
clock=pygame.time.Clock()
# pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)

SW = 1000
SH = 800

screen = pygame.display.set_mode((SW,SH))

screen.fill(white)

avatar_data = []
with open("users.tsv","r") as file:
    for line in file:
        line = line.strip()
        arr = line.split("\t")
        if arr[0] == player1 or arr[0] == player2:
            avatar_data.append([arr[0],int(arr[2]),int(arr[3]),int(arr[4]),int(arr[5])])

title = pygame.image.load("../Graphics/Title.png").convert_alpha()
title = pygame.transform.scale(title,(900,250))
loc = []
for i in range(15):
    loc.append(pygame.image.load(f"../Graphics/LOC/LOC{i + 1}.png"))
    loc[-1] = pygame.transform.scale(loc[-1],(15,10 * i + 250))

skins = []
for i in range(5):
    skins.append(pygame.image.load(f"../Graphics/Skins/Skin{i+1}.png").convert_alpha())
    skins[-1] = pygame.transform.scale(skins[-1],(300,315))

eyes = []
for i in range(5):
    eyes.append(pygame.image.load(f"../Graphics/Eyes/Eye{i+1}.png").convert_alpha())
    eyes[-1]  = pygame.transform.scale(eyes[-1],(200,60))

mouths = []
for i in range(5):
    mouths.append(pygame.image.load(f"../Graphics/Mouths/Mouth{i+1}.png").convert_alpha())
    mouths[-1] = pygame.transform.scale(mouths[-1],(150,60))

hats = []
for i in range(5):
    hats.append(pygame.image.load(f"../Graphics/Hats/Hat{i+1}.png").convert_alpha())
    hats[-1] = pygame.transform.scale(hats[-1],(260,135))

frame = 0
par = []
for pos in range(SW // 20):
    par.append([random.choice(loc),100 * random.randint(0,10) , random.randint(4,10), pos])
    par[-1][0].set_alpha(random.randint(200,255))


class Text:
    def __init__(self,text,size,pos,font="calibri",color=white):
        self.text_font = pygame.font.SysFont(font,size)
        self.text_surf = self.text_font.render(text,True,color)
        self.rect = self.text_surf.get_rect(center = pos)
        self.pos = pos
    def render(self,scale=1):
        if scale != 1:
            t=pygame.transform.smoothscale_by((self.text_surf),scale)
            trect = t.get_rect(center=self.pos)
            screen.blit(t,trect)
        else:
            screen.blit(self.text_surf,self.rect)

class Button:
    def __init__(self,location,color=orange,border_color=white,img=None,size = (160,50),sqrscaling = False,border_radius = None,border_width=5):#text=None,fontsize=None,font="calibri",text_color=white
        # if type:
        #     self.type = "text"
        #     #self.text_surf = create_textsurf(text,fontsize,font,text_color,bg_color)
        #     self.text_rect = self.text_surf.get_rect(center = self.location)
        #     self.rect = pygame.Rect(location[0]-size[0]/2,location[1]-size[1]/2,size[0],size[1])
            
        # else:
        #     self.type = "img"
        #     self.img = pygame.image.load(img).convert_alpha()
        #     self.rect = self.img.get_rect(center=self.location)
        self.location = location
        self.size = size
        self.uh = False
        self.assigned = False
        self.scale=1
        self.border_width = border_width
        self.active = True
        self.sqrscaling = sqrscaling
        if img:
            self.img = pygame.transform.smoothscale(pygame.image.load(img).convert_alpha(),size)
            self.og_img = self.img
            self.rect = self.img.get_rect(center=location)
        else:
            self.img = None
            self.color = color
            self.border_color = border_color
            self.rect = pygame.Rect(location[0]-size[0]/2,location[1]-size[1]/2,size[0],size[1])
            if not border_radius:
                self.border_radius = size[1]//2
            else:
                self.border_radius = border_radius
        self.nrect=self.rect
        self.osize = self.size

    def render(self):
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos()) and not(pygame.mouse.get_pressed()[0])
        if self.active:
            if self.hover and not(self.uh):
                if not self.sqrscaling:
                    self.size = (self.osize[0]*1.2,self.osize[1]*1.05)
                else:
                    self.size = (self.osize[0]*1.1,self.osize[1]*1.1)
                self.nrect = pygame.Rect(self.location[0]-self.size[0]/2,self.location[1]-self.size[1]/2,self.size[0],self.size[1])
                if self.img:
                    self.img = pygame.transform.smoothscale(self.og_img,(self.size))
                        
                self.scale=1.05

            if self.uh and not(self.hover):
                self.size = self.osize
                self.nrect = self.rect
                if self.img:
                    self.img = self.og_img
                self.scale=1
        else:
            self.nrect = self.rect
            self.img = self.og_img
        if self.img:
            screen.blit(self.img,self.nrect)
        else:
            pygame.draw.rect(screen,self.color,self.nrect,self.border_width,self.border_radius)

        if self.assigned:
            self.text.render(self.scale)

        self.uh = self.hover

    def assigntext(self,text,fontsize,font="calibri",text_color=white):
        self.assigned = True
        self.text = Text(text,fontsize,self.location,font,text_color)
        
    # def onclick(self,pos):
    #     if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
    #         self.action()

class MenuBar:
    def __init__(self,bg_color = (59,59,59), size = (844,204)):
        POS = self.pos = (SW/2,SH-100)
        self.size = size
        self.color = bg_color
        self.buttons=[
                Button((POS[0]-size[0]//2+160, POS[1]),img = "options_button.png",size=(220,140),border_radius=10),
                Button((SW/2, POS[1]),img="quitbutton.png",size=(220,140),border_radius=10),
                Button((POS[0]+size[0]//2-160, POS[1]),img="playbutton.png",size=(220,140),border_radius=10)
            ]
        self.buttons[0].assigntext("OPTIONS",50,None,(87,236,115))
        self.buttons[1].assigntext("QUIT",50,None,(241,95,95))
        self.buttons[2].assigntext("PLAY",50,None,(61,149,236))
        self.rect = pygame.Rect(0,0,size[0],size[1])
        self.rect.center = POS
        self.active = True
        self.img = pygame.image.load("menurect1.png").convert_alpha()

    def render(self):
        # pygame.draw.rect(screen,self.color,self.rect,0,20)
        screen.blit(self.img,self.rect)
        for b in self.buttons:
            b.render()

class SelectionBar:
    def __init__(self,settings):
        self.settings = settings
        POS=self.POS= (SW/2,SH/2)
        if settings:
            self.buttons=[
                Button((SW/2, POS[1]-200+50),img = "regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+150),img = "regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+250),img = "regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+370),img = "backbutton.png",size=(340,90))
            ]
            self.buttons[0].assigntext("SOUND",30,None)
            self.buttons[1].assigntext("AVATAR",30,None)
            self.buttons[2].assigntext("ANALYTICS",30,None)
            self.buttons[3].assigntext("BACK",30,None,red)
            self.size = (550*968//800,450*968//800)

        else:
            self.buttons = [
                #Button(True,(SW/2, SH/2 - 30),)
                #Button((SW/2, POS[1]-200+50),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+50),img = "regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+130),img = "regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+210),img = "regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+290),img = "regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+370),img = "regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+470),img = "backbutton.png",size=(340,90))
            ]
            self.buttons[0].assigntext("TicTacToe",30,None)
            self.buttons[1].assigntext("Othello",30,None)
            self.buttons[2].assigntext("Connect4",30,None)
            self.buttons[3].assigntext("Chain Reaction",30,None)
            self.buttons[4].assigntext("Checkers",30,None)
            self.buttons[5].assigntext("BACK",30,None,red)
            self.size = (550*968//800,650*968//800)
        self.rect = pygame.Rect(0,0,self.size[0],self.size[1])
        self.rect.center = self.POS
        self.img = pygame.image.load("roundrect.png").convert_alpha()
        self.img = pygame.transform.smoothscale(self.img,(self.size))
    def render(self):
        #render self
        #dark grey rounded rect with neon green border, maybe glow?
        screen.blit(self.img, self.rect)
        for b in self.buttons:
            b.render()

class SoundTrack:
    def __init__(self,filename,songname,):
        self.name = songname
        self.filename = filename
        self.volume = 100
        self.text = Text(songname,45,(SW /2, SH / 2 - 180),None,(8,200,4))
    def load(self):
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play(loops=-1)
    def set_volume(self):
        pygame.mixer.music.set_volume(self.volume/100)


buttons = [
    #Button(True,(SW/2, SH/2 - 30),)
    # Button((SW/2, 200)), #somebutton
    # Button((SW/2,200+100)),
    # Button((SW/2,200+100*2)),
    # Button((SW/2,200+100*3)),
    # Button((SW/2,200+100*4)),
    Button((SW-50,50),img = "back.png",sqrscaling=True,size = (30,30))
]
# buttons[0].assigntext("TicTacToe",30,None)
# buttons[1].assigntext("Othello",30,None)
# buttons[2].assigntext("Connect4",30,None)
# buttons[3].assigntext("Chain Reaction",30,None)
# buttons[4].assigntext("Checkers",30,None)

gamebuttons= [
    buttons[-1]
    #settings
]

soundtracks = [SoundTrack("../Sound/elektronomia.ogg","Elektronomia"),
               SoundTrack("el.ogg","Elektronomia1"),
               SoundTrack("../Sound/cyberpunk.ogg","Ireallywant"),
               SoundTrack("cp.ogg","Cyberpunk 2077")]

player = []
player.append(Text(avatar_data[0][0],45,(SW /2, SH / 2 - 180),None,(8,200,4)))
player.append(Text(avatar_data[1][0],45,(SW /2, SH / 2 - 180),None,(8,200,4)))

analytics_par = []
analytics_par.append(Text("Wins",45,(SW/2,SH/2-80),None,(8,200,4)))
analytics_par.append(Text("Losses",45,(SW/2,SH/2-80),None,(8,200,4)))
analytics_par.append(Text("Win/Loss Ratio",45,(SW/2,SH/2-80),None,(8,200,4)))
analytics_par.append(Text("Total games",45,(SW/2,SH/2-80),None,(8,200,4)))

menu, avatar, sound, analytics=False, False, False, False
game, winframe = None, None
analytics_iter = 0

av1 = parse_avatar(player1) 
av2 = parse_avatar(player2)

avatar_iter = sound_iter = 0
songs = len(soundtracks)
sound_select = False
opacity = pygame.Surface((SW,SH))
opacity.fill((84,84,84))
opacity.set_alpha(171)
menubar = MenuBar()

avatar_rect = pygame.Rect(0,0,550*968//800,600*968//800)
avatar_rect.center = (SW / 2, SH / 2 + 50)
avatar_img  = pygame.transform.smoothscale(pygame.image.load("roundrect.png"),avatar_rect.size)

sound_rect = pygame.Rect(0,0,550*968//800,600*968//800)
sound_rect.center = (SW / 2, SH / 2 + 50)
sound_img = pygame.transform.smoothscale(pygame.image.load("roundrect.png"),sound_rect.size)


while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (gamebuttons[-1].rect.collidepoint(event.pos) and not menu):
                    if not game:
                        pygame.quit()
                        sys.exit()
                    else:
                        game = False

                if not game and not menu:
                    # if buttons[0].rect.collidepoint(event.pos):
                    #     game = TicTacToe("me","ching","me",(10,10),screen)
                    # elif buttons[1].rect.collidepoint(event.pos):
                    #     game = Othello("me","ching","me",(8,8),screen)
                    # elif buttons[4].rect.collidepoint(event.pos):
                    #     game = Checkers("me","ching","me",(8,8),screen)
                    # elif buttons[3].rect.collidepoint(event.pos):
                    #     game = Chain_rxn("me","Ching","me",(6,6,2),screen)
                    # elif buttons[2].rect.collidepoint(event.pos):
                    #     game = Connect4("me","ching","me",(7,7),screen)
                    if menubar.buttons[0].rect.collidepoint(event.pos):
                        menu = SelectionBar(True)
                        for b in menubar.buttons:
                            b.active = False
                            
                        buttons[-1].active = False
                    elif menubar.buttons[1].rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif menubar.buttons[2].rect.collidepoint(event.pos):
                        menu = SelectionBar(False)
                        for b in menubar.buttons:
                            b.active = False
                        buttons[-1].active = False
                    
                elif game and not menu:
                    if winframe is None and game.checkpress(event):
                        game.winner = game.turn
                
                elif not game and menu and menu.settings == False:
                    if menu.buttons[0].rect.collidepoint(event.pos):
                        game = TicTacToe(player1,player2,player1,(10,10),screen)
                        menu=False
                    elif menu.buttons[1].rect.collidepoint(event.pos):
                        game = Othello(player1,player2,player1,(8,8),screen)
                        menu=False
                    elif menu.buttons[4].rect.collidepoint(event.pos):
                        game = Checkers(player1,player2,player1,(8,8),screen)
                        menu=False
                    elif menu.buttons[3].rect.collidepoint(event.pos):
                        game = Chain_rxn(player1,player2,player1,(6,6,2),screen)
                        menu=False
                    elif menu.buttons[2].rect.collidepoint(event.pos):
                        game = Connect4(player1,player2,player1,(7,7),screen)
                        menu=False
                    elif menu.buttons[5].rect.collidepoint(event.pos):
                        menu = False
                        for b in menubar.buttons:
                            b.active = True
                        buttons[-1].active = True
                
                elif not game and menu and menu.settings == True:
                    if analytics:
                        if analytics_buttons[0].rect.collidepoint(event.pos):
                            analytics_iter = (analytics_iter - 1) % 4
                        elif analytics_buttons[1].rect.collidepoint(event.pos):
                            analytics_iter = (analytics_iter + 1) % 4
                        elif analytics_show.rect.collidepoint(event.pos):
                            os.system(f"bash leaderboard.sh {analytics_iter + 1}")
                        elif analytics_quit.rect.collidepoint(event.pos):
                            analytics = False

                    elif avatar:
                        if avatar_buttons[0].rect.collidepoint(event.pos):
                            avatar_iter = (avatar_iter - 1) % 2
                        elif avatar_buttons[1].rect.collidepoint(event.pos):
                            avatar_iter = (avatar_iter + 1) % 2
                        elif avatar_buttons[2].rect.collidepoint(event.pos):
                            avatar_data[avatar_iter][1] = (avatar_data[avatar_iter][1] - 1) % 5
                        elif avatar_buttons[3].rect.collidepoint(event.pos):
                            avatar_data[avatar_iter][1] = (avatar_data[avatar_iter][1] + 1) % 5
                        elif avatar_buttons[4].rect.collidepoint(event.pos):
                            avatar_data[avatar_iter][2] = (avatar_data[avatar_iter][2] - 1) % 5
                        elif avatar_buttons[5].rect.collidepoint(event.pos):
                            avatar_data[avatar_iter][2] = (avatar_data[avatar_iter][2] + 1) % 5
                        elif avatar_buttons[6].rect.collidepoint(event.pos):
                            avatar_data[avatar_iter][3] = (avatar_data[avatar_iter][3] - 1) % 5
                        elif avatar_buttons[7].rect.collidepoint(event.pos):
                            avatar_data[avatar_iter][3] = (avatar_data[avatar_iter][3] + 1) % 5
                        elif avatar_buttons[8].rect.collidepoint(event.pos):
                            avatar_data[avatar_iter][4] = (avatar_data[avatar_iter][4] - 1) % 5
                        elif avatar_buttons[9].rect.collidepoint(event.pos):
                            avatar_data[avatar_iter][4] = (avatar_data[avatar_iter][4] + 1) % 5
                        elif avatar_quit.rect.collidepoint(event.pos):
                            os.system(f"sed -i 's/{avatar_data[0][0]}\\t\\(.*\\)\\t.\\t.\\t.\\t./{avatar_data[0][0]}\\t\\1\\t{avatar_data[0][1]}\\t{avatar_data[0][2]}\\t{avatar_data[0][3]}\\t{avatar_data[0][4]}/' users.tsv")
                            os.system(f"sed -i 's/{avatar_data[1][0]}\\t\\(.*\\)\\t.\\t.\\t.\\t./{avatar_data[1][0]}\\t\\1\\t{avatar_data[1][1]}\\t{avatar_data[1][2]}\\t{avatar_data[1][3]}\\t{avatar_data[1][4]}/' users.tsv")
                            avatar = False
                            av1 = parse_avatar(player1) 
                            av2 = parse_avatar(player2)#REPLACE THIS SHIT
                    
                    elif sound:
                        if sound_buttons[0].rect.collidepoint(event.pos):
                            sound_iter = (sound_iter - 1) % songs
                            soundtracks[sound_iter].load()
                        elif sound_buttons[1].rect.collidepoint(event.pos):
                            sound_iter = (sound_iter + 1) % songs
                            soundtracks[sound_iter].load()
                        elif sound_buttons[2].rect.collidepoint(event.pos):
                            if soundtracks[sound_iter].volume>0:
                                soundtracks[sound_iter].volume-=1
                                soundtracks[sound_iter].set_volume()
                        elif sound_buttons[3].rect.collidepoint(event.pos):
                            if soundtracks[sound_iter].volume<100:
                                soundtracks[sound_iter].volume+=1
                                soundtracks[sound_iter].set_volume()
                        elif sound_quit.rect.collidepoint(event.pos):
                            sound = False

                    elif menu.buttons[0].rect.collidepoint(event.pos):
                        sound = True
                        sound_select = True
                        soundtracks[sound_iter].load()
                        sound_quit = Button((SW/2,SH/2+280),img = "backbutton.png",size=(340,90))
                        sound_quit.assigntext("DONE",30,None,red)
                        sound_buttons = []
                        for i in range(4):
                            #sound_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-180+90*(i//2)),color=(8, 69, 4),border_width=0,size=(40,90)))
                            if i % 2 == 0:
                                #sound_buttons[-1].assigntext("<",30,None)
                                sound_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-180+90*(i//2)),img="leftbutton.png",border_width=0,size=(65,69),sqrscaling=True))
                            else:
                                #sound_buttons[-1].assigntext(">",30,None)
                                sound_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-180+90*(i//2)),img="rightbutton.png",border_width=0,size=(65,69),sqrscaling=True))

                    elif menu.buttons[1].rect.collidepoint(event.pos):
                        avatar = True
                        avatar_quit = Button((SW/2,SH/2+280),img = "backbutton.png",size=(340,90))
                        avatar_quit.assigntext("DONE",30,None,red)
                        avatar_buttons = []
                        for i in range(10):
                            # avatar_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-180+90*(i//2)),color=(8, 69, 4),border_width=0,size=(40,90)))
                            if i % 2 == 0:
                                #avatar_buttons[-1].assigntext("<",30,None)
                                avatar_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-180+90*(i//2)),img="leftbutton.png",border_width=0,size=(65,69),sqrscaling=True))
                            else:
                                #avatar_buttons[-1].assigntext(">",30,None)
                                avatar_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-180+90*(i//2)),img="rightbutton.png",border_width=0,size=(65,69),sqrscaling = True))

                    elif menu.buttons[2].rect.collidepoint(event.pos):
                        analytics = True
                        analytics_quit = Button((SW/2,SH/2+230),color=(8,69,4),border_width=0,size=(350,50))
                        analytics_quit.assigntext("DONE",30,None,red)
                        analytics_show = Button((SW/2,SH/2 + 150),color=(8,69,4),border_width=0,size=(350,50))
                        analytics_show.assigntext("SHOW",30,None,red)
                        analytics_buttons = []
                        for i in range(2):
                            analytics_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-80),color=(8,69,4),border_width=0,size=(40,90)))
                            if i % 2 == 0:
                                analytics_buttons[-1].assigntext("<",30,None)
                            else:
                                analytics_buttons[-1].assigntext(">",30,None)
                        # pass#analytics
                        #DO NOT PRESS
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

                    elif menu.buttons[3].rect.collidepoint(event.pos):
                        menu = False
                        for b in menubar.buttons:
                            b.active = True
                        buttons[-1].active = True


    screen.fill((0,0,0))
    for i in range(SW // 20):
        screen.blit(par[i][0],(20 * par[i][3] , SH - (frame * par[i][2] + par[i][1]) % (2 * SH)))
        screen.blit(par[(i + 3) % (SW // 20)][0],(20 * par[i][3] , SH - (frame * par[i][2] + SH / 2 + par[i][1]) % (2 * SH)))
        screen.blit(par[(i + 7) % (SW // 20)][0],(20 * par[i][3] , SH - (frame * par[i][2] + SH  + par[i][1]) % (2 * SH)))
        screen.blit(par[(i + 8) % (SW // 20)][0],(20 * par[i][3] , SH - (frame * par[i][2] + 3 * SH / 2 + par[i][1]) % (2 * SH)))
    frame = (frame - 1) % (2 * SH)

    if not game:
        screen.blit(title,(SW/2 - 450, 150))
        for b in buttons:
            b.render()
        menubar.render()
        avatar_render(av1,(50,20),screen,scale = 0.16)
        avatar_render(av2,(120,20),screen,scale = 0.16)
        
    else:
        game.renderboard("fah")
        for b in gamebuttons:
            b.render()
        if game.winner:
            if winframe is None:
                winframe = frame
            elif (winframe - frame) % (2 * SH) == 120:
                game = False
                winframe = None

    if menu:
        screen.blit(opacity,(0,0))
        #include settings rendering func here
        if avatar == True:
            #pygame.draw.rect(screen,(59,59,59),avatar_rect,0,20)
            screen.blit(avatar_img,avatar_rect)
            avatar_quit.render()
            for b in avatar_buttons:
                b.render()
            player[avatar_iter].render()
            screen.blit(skins[avatar_data[avatar_iter][4]],(SW / 2 - 150, SH / 2 - 90))
            screen.blit(hats[avatar_data[avatar_iter][1]],(SW / 2 - 130, SH / 2 - 175))
            screen.blit(eyes[avatar_data[avatar_iter][2]],(SW / 2 - 100, SH / 2 - 20))
            screen.blit(mouths[avatar_data[avatar_iter][3]],(SW / 2 - 75, SH / 2 + 60))

        elif analytics == True:
            analytics_rect = pygame.Rect(0,0,550,600)
            analytics_rect.center = (SW/2,SH/2)
            pygame.draw.rect(screen,(59,59,59),analytics_rect,0,20)
            analytics_show.render()
            analytics_quit.render()
            for b in analytics_buttons:
                b.render()
            analytics_par[analytics_iter].render()

        elif sound:
            #pygame.draw.rect(screen,(59,59,59),sound_rect,0,20)
            screen.blit(sound_img,sound_rect)
            sound_quit.render()
            for b in sound_buttons:
                b.render()
            soundtracks[sound_iter].text.render()
            Text(str(soundtracks[sound_iter].volume),45,(SW / 2, SH / 2 - 90)).render()
        else:
            menu.render()

    clock.tick(60)
    pygame.display.flip()

# win/draw,game_name,winner/firstplayer,otherplayer,date(not rn)
########### matplotlib shit
'''
with f as open("history.csv","r",newline=''):
    game_stats = {"tictactoe":0,"othello":0,"connect4":0,"chain_rxn":0,"checkers":0}
    player_wins = {}
    csvreader = csv.reader(f)
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
