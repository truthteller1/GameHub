import pygame
import sys
import time
from games.tictactoe import TicTacToe
from games.connect4 import Connect4
from games.othello import Othello
from games.chain_rxn import Chain_rxn
from games.checkers import Checkers
from games.avatar_render import *
from utilities.analytics import Analytics
from utilities.button import *
from utilities.avatar_menu import *
import matplotlib.pyplot as plt
import csv
import random
import os


white = (255,255,255)
black = (0,0,0)
navy = (1,3,43)
red = (241,95,95)
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

avatar_data = [[],[]]
with open("users.tsv","r") as file:
    for line in file:
        line = line.strip()
        arr = line.split("\t")
        if arr[0] == player1:
            avatar_data[0] = [arr[0],int(arr[2]),int(arr[3]),int(arr[4]),int(arr[5])]
        elif arr[0] == player2:
            avatar_data[1] = [arr[0],int(arr[2]),int(arr[3]),int(arr[4]),int(arr[5])]

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

class MenuBar:
    def __init__(self,bg_color = (59,59,59), size = (844,204)):
        POS = self.pos = (SW/2,SH-100)
        self.size = size
        self.color = bg_color
        self.buttons=[
                Button((POS[0]-size[0]//2+160, POS[1]),screen,img = "../Graphics/optionsbutton.png",size=(220,140)),
                Button((SW/2, POS[1]),screen,img="../Graphics/quitbutton.png",size=(220,140)),
                Button((POS[0]+size[0]//2-160, POS[1]),screen,img="../Graphics/playbutton.png",size=(220,140))
            ]
        self.buttons[0].assigntext("OPTIONS",35,None,(87,236,115))
        self.buttons[1].assigntext("QUIT",35,None,(241,95,95))
        self.buttons[2].assigntext("PLAY",35,None,(61,149,236))
        self.rect = pygame.Rect(0,0,size[0],size[1])
        self.rect.center = POS
        self.active = True
        self.img = pygame.image.load("../Graphics/menurect1.png").convert_alpha()

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
                Button((SW/2, POS[1]-200+50),screen,img = "../Graphics/regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+150),screen,img = "../Graphics/regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+250),screen,img = "../Graphics/regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+370),screen,img = "../Graphics/backbutton.png",size=(340,90))
            ]
            self.buttons[0].assigntext("SOUND",25,None)
            self.buttons[1].assigntext("AVATAR",25,None)
            self.buttons[2].assigntext("ANALYTICS",25,None)
            self.buttons[3].assigntext("BACK",25,None,red)
            self.size = (550*968//800,450*968//800)

        else:
            self.buttons = [
                #Button(True,(SW/2, SH/2 - 30),)
                #Button((SW/2, POS[1]-200+50),color=(8, 69, 4),border_width=0,size=(400,50)),
                Button((SW/2, POS[1]-200+50),screen,img = "../Graphics/regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+130),screen,img = "../Graphics/regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+210),screen,img = "../Graphics/regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+290),screen,img = "../Graphics/regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+370),screen,img = "../Graphics/regularbutton.png",size=(440,90)),
                Button((SW/2, POS[1]-200+470),screen,img = "../Graphics/backbutton.png",size=(340,90))
            ]
            self.buttons[0].assigntext("TicTacToe",25,None)
            self.buttons[1].assigntext("Othello",25,None)
            self.buttons[2].assigntext("Connect4",25,None)
            self.buttons[3].assigntext("Chain Reaction",25,None)
            self.buttons[4].assigntext("Checkers",25,None)
            self.buttons[5].assigntext("BACK",25,None,red)
            self.size = (550*968//800,650*968//800)
        self.rect = pygame.Rect(0,0,self.size[0],self.size[1])
        self.rect.center = self.POS
        self.img = pygame.image.load("../Graphics/roundrect.png").convert_alpha()
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
        self.text = Text(songname,35,(SW /2, SH / 2 - 140),screen,None,(87,236,115))
    def load(self):
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play(loops=-1)
    def set_volume(self):
        pygame.mixer.music.set_volume(self.volume/100)


buttons = [
    Button((SW-50,50),screen,img = "../Graphics/back.png",sqrscaling=True,size = (30,30))
]

gamebuttons= [
    buttons[-1]
    #settings
]

soundtracks = [
    SoundTrack("../Sound/elektronomia.ogg","Elektronomia"),
    SoundTrack("el.ogg","Elektronomia1"),
    SoundTrack("../Sound/cyberpunk.ogg","Ireallywant"),
    SoundTrack("cp.ogg","Cyberpunk 2077")
    ]

player = []
player.append([Text(avatar_data[0][0],30,(SW /2, SH / 2 - 190),screen,None,(87,236,115)),parse_avatar(avatar_data[0][0])])
player.append([Text(avatar_data[1][0],30,(SW /2, SH / 2 - 190),screen,None,(87,236,115)),parse_avatar(avatar_data[1][0])])

analytics_par = []
analytics_par.append(Text("Wins",35,(SW/2,SH/2-80),screen,None,(87,236,115)))
analytics_par.append(Text("Losses",35,(SW/2,SH/2-80),screen,None,(87,236,115)))
analytics_par.append(Text("Win/Loss Ratio",35,(SW/2,SH/2-80),screen,None,(87,236,115)))
analytics_par.append(Text("Total games",35,(SW/2,SH/2-80),screen,None,(87,236,115)))
analytics_par.append(Text("Draws",35,(SW/2,SH/2-80),screen,None,(87,236,115)))

menu, avatar, sound, analytics=False, False, False, False
game, winframe = None, None

av1 = player[0][1] 
av2 = player[1][1]

avatar_iter = sound_iter = 0
songs = len(soundtracks)
sound_select = False
opacity = pygame.Surface((SW,SH))
opacity.fill((84,84,84))
opacity.set_alpha(171)
menubar = MenuBar()

avatar_rect = pygame.Rect(0,0,550*968//800,600*968//800)
avatar_rect.center = (SW / 2, SH / 2 + 50)
avatar_img  = pygame.transform.smoothscale(pygame.image.load("../Graphics/roundrect.png"),avatar_rect.size)

sound_rect = pygame.Rect(0,0,550*968//800,440*968//800)
sound_rect.center = (SW / 2, SH / 2 )
sound_img = pygame.transform.smoothscale(pygame.image.load("../Graphics/roundrect.png"),sound_rect.size)

draw_text = Text("Draw",50,(SW/2,300),screen,color=(87,236,115))


while True:
    #EVENT HANDLING
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
                        if game.winner != -1:
                            with open("history.csv","a",newline="") as file:
                                writer = csv.writer(file,quoting=csv.QUOTE_NONE,dialect="unix")
                                game_name = str(type(game))
                                game_name = game_name[game_name.find(".")+1:]
                                game_name = game_name[:game_name.find(".")]
                                writer.writerow(["Win",game_name,game.rep[game.winner],game.rep[3 - game.winner]])
                        else:
                            with open("history.csv","a",newline="") as file:
                                writer = csv.writer(file,quoting=csv.QUOTE_NONE,dialect="unix")
                                game_name = str(type(game))
                                game_name = game_name[game_name.find(".")+1:]
                                game_name = game_name[:game_name.find(".")]
                                writer.writerow(["Draw",game_name,game.rep[1],game.rep[2]])
                
                elif not game and menu and menu.settings == False:
                    if menu.buttons[0].rect.collidepoint(event.pos):
                        menu = False
                        game = TicTacToe(player1,player2,player1,(10,10),screen)
                    elif menu.buttons[1].rect.collidepoint(event.pos):
                        menu = False
                        game = Othello(player1,player2,player1,(8,8),screen)
                    elif menu.buttons[4].rect.collidepoint(event.pos):
                        menu = False
                        game = Checkers(player1,player2,player1,(8,8),screen)
                    elif menu.buttons[3].rect.collidepoint(event.pos):
                        menu = False
                        game = Chain_rxn(player1,player2,player1,(6,6,2),screen)
                    elif menu.buttons[2].rect.collidepoint(event.pos):
                        menu = False
                        game = Connect4(player1,player2,player1,(7,7),screen)
                    elif menu.buttons[5].rect.collidepoint(event.pos):
                        menu = False
                        for b in menubar.buttons:
                            b.active = True
                        buttons[-1].active = True
                
                elif not game and menu and menu.settings == True:
                    if analytics:
                        if leaderboard.interact(event):
                            if winframe:
                                winframe = None
                                menu = SelectionBar(False)
                            analytics = False

                    elif avatar:
                        if AvatarMenu.interact(event,avatar_data):
                            avatar = False
                            av1 = parse_avatar(player1) 
                            av2 = parse_avatar(player2)#REPLACE THIS SHIT
                            player[0][1] = av1
                            player[1][1] = av2
                    
                    elif sound:
                        if sound_buttons[0].rect.collidepoint(event.pos):
                            sound_iter = (sound_iter - 1) % songs
                            soundtracks[sound_iter].load()
                        elif sound_buttons[1].rect.collidepoint(event.pos):
                            sound_iter = (sound_iter + 1) % songs
                            soundtracks[sound_iter].load()
                        elif sound_buttons[2].rect.collidepoint(event.pos):
                            soundtracks[sound_iter].volume=(soundtracks[sound_iter].volume-1)%101
                            soundtracks[sound_iter].set_volume()
                        elif sound_buttons[3].rect.collidepoint(event.pos):
                            soundtracks[sound_iter].volume=(soundtracks[sound_iter].volume+1)%101
                            soundtracks[sound_iter].set_volume()
                        elif sound_quit.rect.collidepoint(event.pos):
                            sound = False

                    elif menu.buttons[0].rect.collidepoint(event.pos):
                        sound = True
                        sound_select = True
                        soundtracks[sound_iter].load()
                        sound_quit = Button((SW/2,SH/2+160),screen,img = "../Graphics/backbutton.png",size=(340,90))
                        sound_quit.assigntext("DONE",30,None,red)
                        sound_buttons = []
                        for i in range(4):
                            if i % 2 == 0:
                                sound_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-140+90*(i//2)),screen,img="../Graphics/leftbutton.png",border_width=0,size=(65,69),sqrscaling=True))
                            else:
                                sound_buttons.append(Button((SW/2-((-1)**i)*200,SH/2-140+90*(i//2)),screen,img="../Graphics/rightbutton.png",border_width=0,size=(65,69),sqrscaling=True))

                    elif menu.buttons[1].rect.collidepoint(event.pos):
                        avatar = True
                        AvatarMenu = Avatar(SW,SH,screen)

                    elif menu.buttons[2].rect.collidepoint(event.pos):
                        analytics = True
                        leaderboard = Analytics(SW,SH,screen)

                    elif menu.buttons[3].rect.collidepoint(event.pos):
                        menu = False
                        for b in menubar.buttons:
                            b.active = True
                        buttons[-1].active = True

    #### RENDERING
    
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

            elif (winframe - frame) % (2 * SH) >= 60:
                if (winframe - frame) % (2 * SH) <= 240:
                    screen.blit(opacity,(0,0))
                    win_rect = pygame.Rect(0,0,550*968//800,600*968//800)
                    win_rect.center = (SW/2,SH/2)
                    # pygame.draw.rect(screen,(59,59,59),win_rect,0,20)
                    screen.blit(avatar_img,win_rect)
                    if game.winner != -1:
                        avatar_render(player[game.winner - 1][1],(SW/2,SH/2-120),screen)
                    else:
                        avatar_render(player[0][1],(SW/2 - 75,SH/2-40),screen,scale=0.5)
                        avatar_render(player[1][1],(SW/2+75,SH/2-90),screen,scale=0.5)
                else:
                    menu = SelectionBar(True)
                    for b in menubar.buttons:
                        b.active = False
                    analytics = True
                    leaderboard = Analytics(SW,SH,screen)
                    game = False
                    winframe = True

    if menu:
        screen.blit(opacity,(0,0))

        if avatar == True:
            screen.blit(avatar_img,avatar_rect)
            AvatarMenu.avatar_quit.render()
            for b in AvatarMenu.avatar_buttons:
                b.render()
            player[AvatarMenu.avatar_iter][0].render()
            screen.blit(skins[avatar_data[AvatarMenu.avatar_iter][4]],(SW / 2 - 150, SH / 2 - 90))
            screen.blit(hats[avatar_data[AvatarMenu.avatar_iter][1]],(SW / 2 - 130, SH / 2 - 175))
            screen.blit(eyes[avatar_data[AvatarMenu.avatar_iter][2]],(SW / 2 - 100, SH / 2 - 20))
            screen.blit(mouths[avatar_data[AvatarMenu.avatar_iter][3]],(SW / 2 - 75, SH / 2 + 60))

        elif analytics == True:
            analytics_rect = pygame.Rect(0,0,550*968//800,600*968//800)
            analytics_rect.center = (SW/2,SH/2)
            screen.blit(avatar_img, analytics_rect)
            leaderboard.analytics_show.render()
            leaderboard.analytics_quit.render()
            for b in leaderboard.analytics_buttons:
                b.render()
            analytics_par[leaderboard.analytics_iter].render()

        elif sound:
            screen.blit(sound_img,sound_rect)
            sound_quit.render()
            for b in sound_buttons:
                b.render()
            soundtracks[sound_iter].text.render()
            Text(str(soundtracks[sound_iter].volume),30,(SW / 2, SH / 2 - 50),screen).render()

        else:
            menu.render()
    
    clock.tick(60)
    pygame.display.flip()
