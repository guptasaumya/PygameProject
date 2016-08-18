import pygame, random, sys     #import modules
from pygame.locals import*
pygame.init()

black = (0,0,0)     #initialize global variables
white = (255,255,255)
fps = 25
topscore = 0
gamescounter = 0
addnewflamerate = 40
window_height = 600
window_width = 1200

class dragon:     #represents the dragon       
    global firerect,image,imagerect,catusrect
    up = False
    down = True
    velocity = 15
    def __init__(self):    #function to make the dragon object
        self.image = load_image('dragon.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.centery = window_height/2
        self.imagerect.right = window_width - 20
    def update(self):     #function to move the dragon in verical direction at a paticular velocity between the cactus and the fire
        if self.imagerect.top < cactusrect.bottom:
            self.down = True
            self.up = False
        if self.imagerect.bottom > firerect.top:
            self.up = True
            self.down = False
        if self.up:
            self.imagerect.top -= self.velocity
        if self.down:
            self.imagerect.bottom += self.velocity
    def return_height(self):     #function that returns the height of the dragon at any time
        return self.imagerect.top

class flames:     #represents a flame
    global image,imagerect
    flamespeed = 15
    left = True
    def __init__(self):     #function to make a flame object generated from the height of the dragon object
        self.image = load_image('fireball.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.centery = Dragon.return_height()
        self.imagerect.right = window_width - 20
    def update(self):     #function to move the flame object in the left direction and detect whether the flame has reached the end of the screen
        if self.imagerect.left >= 10:
            self.left = True
        if self.left:
            self.imagerect.left -= self.flamespeed
    def collision(self):     #funtion to check the collision of the player with the flame object
        if ((self.imagerect.left < player.imagerect.right) and (((self.imagerect.top > player.imagerect.top) and (self.imagerect.bottom < player.imagerect.bottom)) or ((self.imagerect.top < player.imagerect.top) and (self.imagerect.bottom > player.imagerect.top)) or ((self.imagerect.top < player.imagerect.bottom) and (self.imagerect.bottom > player.imagerect.bottom)))):
            return True
       
class maryo:     #represents the player
    global firerect,image,imagerect,catusrect,moveup,movedown,gravity
    speed = 10
    downspeed = 15
    score = 0
    def __init__(self):     #function to make the player object
        self.image = load_image('maryo.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.centery = window_height/2
        self.imagerect.left = 30
    def update(self):     #function to move the player only when the the player is whithin the range of the movement, i.e. between the cactus and fire  
        if (self.moveup and (self.imagerect.top > cactusrect.bottom)):
            self.imagerect.top -= self.speed
            self.score += 1
        if (self.movedown and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.speed
            self.score += 1
        if (self.gravity and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.downspeed

def terminate():     #to end the program
    pygame.quit()
    sys.exit()

def waitforkey():     #to detect the key press
    while True:     #to wait for the user to start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:     #to terminate if the user presses the escape key
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

def flamehitsmaryo(flames):     #to check if the flame has hit maryo or not
    for f in flames:
        if f.collision():
            return True
        return False
        
def drawtext(text,font,surface,x,y):     #to display text on the screen
    textobj = font.render(text,1,white)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.top = y
    surface.blit(textobj,textrect)

def check_level(score):     #to check the level
    global level
    if score in range (0,250):
        level = 1
    elif score in range (250,500):
        level = 2
    elif score in range (500,750):
        level = 3
    elif score in range (750,1000):
        level = 4
    elif score in range (1000,1250):
        level = 5
   
def load_image(imagename):     #to load images
    image = pygame.image.load(imagename)
    return image

Canvas = pygame.display.set_mode((window_width,window_height))     #set up the screen
pygame.display.set_caption('Maryo')

mainClock = pygame.time.Clock()     #set up the clock 

titlefont = pygame.font.SysFont(None,30,True,False)     #set font object for title
datafont = pygame.font.SysFont(None,20,True,False)     #set font object for data

startimage = load_image('start.png')     #set up the starimage
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2

endimage = load_image('end.png')     #set up the endimage
endimagerect = endimage.get_rect()
endimagerect.centerx = window_width/2
endimagerect.centery = window_height/2

cactus = load_image('cactus_bricks.png')     #define a rect object for cactus
cactusrect = cactus.get_rect()

fire = load_image('fire_bricks.png')     #define a rect object for fire
firerect = fire.get_rect()

pygame.mixer.music.load('mario_theme.wav')     #load and play the bg music
pygame.mixer.music.play(-1,0.0)

Canvas.fill(black)
Canvas.blit(startimage,startimagerect)     #overlap the startimage
pygame.display.update()
waitforkey()
Dragon = dragon()     #instantiate the dragon class

while True:
    if gamescounter != 0:     #to check if it is the first game 
        pygame.mixer.music.load('mario_theme.wav')
        pygame.mixer.music.play(-1,0.0)
        
    level = 1     #initialize variables for each new game
    flame_list = []     #create a list of the flames
    flameaddcounter = 0
    cactusrect.bottom = 50
    firerect.top = window_height - 50
    player = maryo()     #instante the maryo class
    player.moveup = player.movedown = player.gravity = False
    
    while True:     #begin the main loop
        for event in pygame.event.get():     #handle the event
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_UP:
                    player.moveup = True
                    player.movedown = False
                    player.gravity = False
                if event.key == pygame.K_DOWN:
                    player.moveup = False
                    player.movedown = True
                    player.gravity = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.moveup = False
                    player.movedown = False
                    player.gravity = True
                if event.key == pygame.K_DOWN:
                    player.moveup = False
                    player.movedown = False
                    player.gravity = True
                    
        flameaddcounter += 1     #updating the counter
        
        levelchange = level     #storing the previous value of level
        check_level(player.score)
        if levelchange != level:     #updating values if the level has changed
            cactusrect.bottom += 25
            firerect.top -= 25
            
        if flameaddcounter == addnewflamerate:     #condition to create a new flame
            flameaddcounter = 0
            newflame = flames()     #instantiate the flames class in a loop
            flame_list.append(newflame)     #adding the new flame object created to the list
            
        for f in flame_list:    #loop to move all the flames in the left direction
            f.update()
            
        for f in flame_list:    #loop to remove the flame that has reached the end from the list
            if f.imagerect.left == 10:     #condition to remove flame
                flame_list.remove(f)
                
        player.update()     #update position of player
        Dragon.update()     #update position of dragon
        
        Canvas.fill(black)
        Canvas.blit(cactus,cactusrect)     #overlap all the updated and non-updated images and hence fill the screen
        Canvas.blit(fire,firerect)
        Canvas.blit(player.image,player.imagerect)
        Canvas.blit(Dragon.image,Dragon.imagerect)
        
        drawtext('Maryo',titlefont,Canvas,(window_width/2),cactusrect.bottom + 10)     #pass the title text
        text = 'Score : '+str(player.score)+' | Top score : '+str(topscore)+' | Level : '+str(level)
        drawtext(text,datafont,Canvas,window_width/2,cactusrect.bottom + 50)     #pass the data text

        for f in flame_list:     #update psitions of all the flames
            Canvas.blit(f.image,f.imagerect)

        if flamehitsmaryo(flame_list):     #check for flame collision
            if player.score > topscore:
                topscore = player.score     #update the topscore
            break

        if ((player.imagerect.bottom >= firerect.top) or (player.imagerect.top <= cactusrect.bottom)):     #check for bottom and top collision
            if player.score > topscore:
                topscore = player.score
            break
        
        mainClock.tick(fps)     #set the ticks 
        pygame.display.update()
        
    pygame.mixer.music.load('mario_dies.wav')      #load and play the gameover music
    pygame.mixer.music.play(0,0.0)

    Canvas.blit(endimage,endimagerect)     #overlap the end image
    pygame.display.update()
    waitforkey()
    gamescounter += 1      #update the game counter after the keypress


