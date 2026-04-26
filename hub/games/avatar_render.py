import pygame


#POS IS MIDTOP OF THE WHOLE AVATAR!!!!
def avatar_render(img_list,pos,screen,transparency=255,scale=1,player=None): #img_list: 0-skin 1-hat 2-eyes 3-mouth
    img_rects = [None]*4
    img_bl = list(img_rects)
    x,y = pos
    if (player is None):
        for i in range(len(img_list)):
            img_bl[i] = pygame.transform.smoothscale_by(img_list[i], scale)
            img_bl[i].set_alpha(transparency)
            img_rects[i] = img_bl[i].get_rect()
        img_rects[0].midtop = (x,y+70*scale)
        img_rects[1].midtop = (x,y)
        img_rects[2].midtop = (x,y+140*scale)
        img_rects[3].midtop = (x,y+220*scale)
        for i in range(len(img_list)):
            screen.blit(img_bl[i],img_rects[i])

def parse_avatar(player):
    img_list = [None]*4
    with open("users.tsv","r") as file:
        for line in file:
            line = line.strip()
            arr = line.split("\t")
            if arr[0] == player:
                avatar_data=[int(arr[2]),int(arr[3]),int(arr[4]),int(arr[5])]
                break #HATS EYES MOUTH SKIN
        else:
            return None
    img_list[0]=pygame.transform.smoothscale(pygame.image.load(f"../Graphics/Skins/Skin{avatar_data[3]+1}.png").convert_alpha(),(300,315))
    img_list[2]=pygame.transform.smoothscale(pygame.image.load(f"../Graphics/Eyes/Eye{avatar_data[1]+1}.png").convert_alpha(),(200,60))
    img_list[3]=pygame.transform.smoothscale(pygame.image.load(f"../Graphics/Mouths/Mouth{avatar_data[2]+1}.png").convert_alpha(),(150,60))
    img_list[1]=pygame.transform.smoothscale(pygame.image.load(f"../Graphics/Hats/Hat{avatar_data[0]+1}.png").convert_alpha(),(200,80))
    return img_list

