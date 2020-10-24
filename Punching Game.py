import pygame
from random import randint
import time 
import os 
pygame.init()

WIDTH = 300
HEIGHT = 600
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW = (255, 255, 0)
SILVER = (192, 192, 192)
BROWN = (128,  0,   0)
COLOURS = [WHITE,BLUE,GREEN,RED,YELLOW,SILVER,BROWN]
combo_punches = ["single","double","triple"]

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("cod")
clock = pygame.time.Clock()

#External Images

game_folder = os.path.dirname(__file__)
asset_folder = os.path.join(game_folder, 'assets')

def scaleimage(width,height,img):
    image = pygame.image.load(os.path.join(asset_folder, img)).convert()
    image = pygame.transform.scale(image, (width, height))
    return image

option_border = scaleimage(300,100,"borde.png")

bag = scaleimage(80,120,"bag.png")
man = scaleimage(60,120,"man.png")
background = scaleimage(400,600,"background.png")
dojo = scaleimage(400,600,"mountain.png")
master = scaleimage(200,200,"master.png")
belt = scaleimage (200,100,"belt.png")
punchsound = pygame.mixer.Sound(os.path.join(asset_folder, 'punchsound.wav'))

#Texts 

def textrect(text,x,y):
    textbox = text.get_rect()
    textbox.centerx = x
    textbox.centery = y
    screen.blit(text,textbox)
    
textfont = pygame.font.SysFont("mvboli",20,True,False)
textfont1 = pygame.font.SysFont("simsunextb",10,True,False)
fontt = pygame.font.SysFont("microsoftyaheimicrosoftyaheiui",40,True,True)
easytext = textfont.render("easy mode", True, BLACK)
mediumtext = textfont.render("medium mode",True, BLACK)
hardtext = textfont.render("dojo mode", True, BLACK)
continuetext = textfont.render("Continue", True, YELLOW)
endscreentext = textfont.render("You Broke The Bag!", True, YELLOW)
wintext = textfont.render("Nice!", True, YELLOW)
introtext = textfont.render("d O j O", True, BLACK)
winningtext = textfont.render("YOU ARE d O j O sensei",True, YELLOW)
losingtext = textfont.render("PRACTICE IS THE KEY", True, YELLOW)





#Sprites

class wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bag
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH/2) - 50
        self.rect.centery = 450

class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = man
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = 480
        self.counter = 0 
        self.timing = 0
        self.difficulty = ""
        self.scores = []
        self.punchcounter = 0
    

class option1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = option_border
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.centery = 300
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)

class option2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = option_border
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.centery = 150

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class option3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = option_border
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.centery = 450

    def draw(self,screen):
        screen.blit(self.image,self.rect)
            

player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = player()
wall = wall()
option1 = option1()
option2 = option2()
option3 = option3()

#Game Loops

def restart():
    player.punchcounter = 0
    player.counter = 0
    player.scores = []
    for x in all_sprites:
        x.kill()
    starttime = time.time()
    player.rect.centerx = WIDTH/2 



def menu():
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseposx, mouseposy = pygame.mouse.get_pos()
                if (option2.rect.left + 1) <= mouseposx and (option2.rect.right - 1) >= mouseposx and (option2.rect.top - 1) <= mouseposy and (option2.rect.bottom + 1) >= mouseposy:
                    player.difficulty = "hard"
                    game()
                elif (option1.rect.left + 1) <= mouseposx and (option1.rect.right - 1) >= mouseposx and (option1.rect.top - 1) <= mouseposy and (option1.rect.bottom + 1) >= mouseposy:
                    player.difficulty = "medium"
                    game()
                elif (option3.rect.left + 1) <= mouseposx and (option3.rect.right - 1) >= mouseposx and (option3.rect.top - 1) <= mouseposy and (option3.rect.bottom + 1) >= mouseposy:
                    player.difficulty = "easy"
                    game()
        
        screen.blit(dojo,[-100,0])
        textrect(introtext,WIDTH/2,50)
        textrect(hardtext,option2.rect.centerx, option2.rect.centery)
        textrect(mediumtext,option1.rect.centerx,option1.rect.centery)
        textrect(easytext,option3.rect.centerx,option3.rect.centery)
        option1.draw(screen)
        option2.draw(screen)
        option3.draw(screen)
        pygame.display.flip()

def lose():
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseposx, mouseposy = pygame.mouse.get_pos()
                if (option2.rect.left + 1) <= mouseposx and (option2.rect.right - 1) >= mouseposx and (option2.rect.top - 1) <= mouseposy and (option2.rect.bottom + 1) >= mouseposy:
                    menu()
        screen.fill(BLACK)
        textrect(continuetext,option2.rect.centerx, option2.rect.centery)
        textrect(endscreentext,WIDTH/2,50)
        option2.draw(screen)
        pygame.display.flip()


def win():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseposx, mouseposy = pygame.mouse.get_pos()
                if (option2.rect.left + 1) <= mouseposx and (option2.rect.right - 1) >= mouseposx and (option2.rect.top - 1) <= mouseposy and (option2.rect.bottom + 1) >= mouseposy:
                    menu()
        screen.fill(BLACK)
        screen.blit(master,[100,300])
        textrect(continuetext,option2.rect.centerx, option2.rect.centery)
        wintext1 = textfont.render("Timing: " + str(player.timing) + "s", True, YELLOW)
        if player.difficulty == "easy" and player.timing > 2:
            failtext = textfont.render("TOO SLOW! 2s and BELOW", True, YELLOW)
            textrect(failtext,WIDTH/2,50)
            textrect(wintext1,WIDTH/2,75)
        elif player.difficulty == "medium":
            failtext1 = textfont.render("Ready for d O j O?", True, YELLOW)
            textrect(failtext1,WIDTH/2,80)
            textrect(wintext1,WIDTH/2,50)
        else:
            textrect(wintext,WIDTH/2,50)
            textrect(wintext1,WIDTH/2,75)

        
        option2.draw(screen)
        pygame.display.flip()

def hard_win():
    total_time = 0
    for x in player.scores: 
        total_time += x 
    punch_second = 1.5
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseposx, mouseposy = pygame.mouse.get_pos()
                if (option1.rect.left + 1) <= mouseposx and (option1.rect.right - 1) >= mouseposx and (option1.rect.top - 1) <= mouseposy and (option1.rect.bottom + 1) >= mouseposy:
                    restart()
                    menu()
        screen.fill(BLACK)
        hardtext1 = textfont.render("Here are your timings: ", True, YELLOW)
        hardtext3 = textfont.render(str(player.scores[0]) + "s, " + str(player.scores[1])+ "s, " + str(player.scores[2])+ "s, " + str(player.scores[3])+ "s, " + str(player.scores[4])+ "s",True, YELLOW)
        hardtext2 = textfont.render("Total time taken: " + str(total_time) + "s",True,YELLOW)
        textrect(hardtext1,WIDTH/2,70)
        textrect(hardtext2,WIDTH/2,400)
        textrect(hardtext3, WIDTH/2,90)
        textrect(continuetext,option1.rect.centerx,option1.rect.centery)
        if (player.punchcounter * punch_second) > total_time:
            textrect(winningtext,WIDTH/2,360)
            screen.blit(belt,[50,500])
        else:
            textrect(losingtext,WIDTH/2,360)
        option1.draw(screen)
        pygame.display.flip()



def game(): 
    wall_group.add(wall)
    player_group.add(player)
    all_sprites.add(player)
    all_sprites.add(wall)
    endtime = []
    starttime = time.time()
    final_punches = 0
    if player.difficulty == "easy":
        combo_punch = combo_punches[0]
        number = randint(0,6)
    elif player.difficulty == "medium":
        combo_punch = combo_punches[randint(0,1)]
        number = randint(4,6)
    elif player.difficulty == "hard":
        combo_punch = combo_punches[randint(0,2)]
        number = randint(0,6)
    if combo_punch == "single":
        final_punches = number * 1
    elif combo_punch == "double":
        final_punches = number * 2
    elif combo_punch == "triple":
        final_punches = number * 3 
    command = textfont.render("do " + str(number) + " " + combo_punch + " punches!!!", True, BROWN)
    hit_once = False
    punch_once = False
    done = False
    append_once = False


    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                restart()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and hit_once == False:
                    hit_once = True 
                    player.rect.centerx -= 33
                    player.counter += 1
                    pygame.mixer.Sound.play(punchsound)
                    pygame.mixer.music.stop()
                elif event.key == pygame.K_SPACE and hit_once == True:
                    punch_once = False
                    hit_once = False
                    player.rect.centerx += 33
        
        punch = pygame.sprite.collide_rect(wall,player)
        if punch:
            if hit_once == True and punch_once == False: 
                punch_once = True
            if hit_once == False:
                punch_once = False
                
        counter = textfont.render("punches: " + str(player.counter), True, BROWN)
        punch = pygame.sprite.collide_rect(wall,player)
        
        
        
        if final_punches == player.counter:
            if append_once == False:
                endtime.append(time.time())
                append_once = True 
            if int(time.time() - endtime[0]) > 1:
                player.rect.centerx = WIDTH/2 
                player.timing = (int(endtime[0] - starttime))
                if player.timing == 0:
                    player.timing = 1

                if player.difficulty == "hard":
                    player.counter = 0 
                    if final_punches == 0:
                        final_punches = 1
                    player.punchcounter += final_punches
                    player.scores.append(player.timing)
                    if len(player.scores) == 5:
                        hard_win()
                    game()
                else:
                    restart()
                    win()
        elif final_punches < player.counter:
            if append_once == False:
                endtime.append(time.time())
                append_once = True 
            player.timing = (int(endtime[0] - starttime))
            restart()
            lose()
        
        screen.blit(background,[0,0])
        textrect(command,WIDTH//2,75)
        if player.difficulty == "hard":
            round_counter = textfont.render("Round " + str(len(player.scores)+1),True,BROWN)
            textrect(round_counter,WIDTH-100,25)
        if player.difficulty == "easy":
            textrect(counter,(WIDTH-100),25)
        player_group.draw(screen)
        wall_group.draw(screen)
        player_group.update()
        wall_group.update()
        clock.tick(60)
        pygame.display.flip()


menu()
pygame.quit()