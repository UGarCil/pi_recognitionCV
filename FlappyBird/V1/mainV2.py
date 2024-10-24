# MODULES
import pygame
import random
import math
from os.path import join as jn

class Game():
    # DATA DEFS
    RES = 128
    IMG_PATH = f"./images/res_{RES}"
    ACCELFORCE = 4
    # GLOBAL FUNCTIONS
    # FD. remap()
    # Signature: float, float, float, float, float -> float
    # purp. rescale a given value
    def remap(value, from1, to1, from2, to2):
        return (value - from1) / (to1 - from1) * (to2 - from2) + from2



    # DD. BG
    # bg = pygame.image.load(str)
    # interp. the background from flappy bird

    class Bg():
        def __init__(self,x,y):
            self.x = x
            self.y = y
            self.image = pygame.image.load(jn(Game.IMG_PATH,"3.png"))
            self.rect = self.image.get_rect()
            self.w = self.image.get_width()
            self.h = self.image.get_height()
            self.updateRect()

        def updateRect(self):
            self.rect.topleft = self.x, self.y

        def draw(self,screen):
            screen.blit(self.image, self.rect)
            self.updateRect()

    # DD. FLAPPY
    # fl = Flappy()
    # interp. a flappy bird
    class Flappy():
        def __init__(self,x,y):
            self.x = x
            self.y = y
            self.images = [pygame.image.load(jn(Game.IMG_PATH,i)) for i in ["0.png"]]
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            # Variables related to angle and direction
            self.angle = 0
            # Variables related to velocity and acceleration
            self.updateRect()
            self.velY = 0
            self.accelY = 0
            self.jump = False

        def updateRect(self):
            self.rect.center = self.x, self.y
            self.timage = pygame.transform.rotate(self.image, self.angle) 
            self.trect = self.timage.get_rect()
            self.trect.center = self.x, self.y


        def updateAccel(self):
            if self.jump:
                self.accelY -= Game.ACCELFORCE
                if self.accelY <= -1.5:
                    self.accelY = -1.5
                self.jump = False
            else:
                self.accelY += 0.1

        def updateVel(self):
            self.updateAccel()
            self.velY += self.accelY
            if self.velY >= 10:
                self.velY = 10
            if self.velY <= -10:
                self.velY = -10

        def updatePosition(self):
            self.updateVel()
            self.y += self.velY


        def draw(self,screen):
            screen.blit(self.timage, self.trect)
            # pygame.draw.rect(screen,"green",self.rect,3)         #visualize the rect component
            self.updateRect()
            self.updatePosition()
            # negative goes down; positive goes up
            # velocity goes from -10 to 10
            # angle goes from 90 to -90. -80 to 80 gives a more natural transition
            self.angle = Game.remap(self.velY,-10,10,80,-80)

    

    # DD. PIPE_BOTTOM
    # pipeB = Pipe_Bottom()
    # interp. a pipe in the game of Flappy bird. If bird touches then gameOver
    class Pipe_Bottom():
        def __init__(self,x,y):
            self.x = x
            self.y = y
            self.image = pygame.image.load(jn(Game.IMG_PATH,"1.png"))
            self.rect = self.image.get_rect()
            self.w = self.image.get_width()
            self.h = self.image.get_height()
            self.updateRect()
        
        def updateRect(self):
            self.rect.topleft = self.x, self.y

        def draw(self,screen):
            screen.blit(self.image, self.rect)
            self.updateRect()


    # DD. PIPE_TOP
    # pipeT = Pipe_Top()
    # interp. a pipe in the game of Flappy bird. If bird touches then gameOver
    class Pipe_Top(Pipe_Bottom):
        def __init__(self,x,y):
            super().__init__(x,y)
            self.image = pygame.image.load(jn(Game.IMG_PATH,"2.png"))
            self.rect = self.image.get_rect()
            self.updateRect()
        
        def updateRect(self):
            self.rect.bottomleft = self.x, self.y


    # DD. GAMEOVER
    # gameOver = bool
    # interp. whether the game is over or not
    gameOver = False

    def __init__(self):
        self.bg0 = Game.Bg(0,0)
        self.bg1 = Game.Bg(self.bg0.x + self.bg0.w, self.bg0.y)
        self.SCREEN = (self.bg0.w, self.bg0.h)
        self.display = pygame.display.set_mode(self.SCREEN)
        self.fl0 = Game.Flappy(self.SCREEN[0]//4, self.SCREEN[1]//2)

        # DD. BGS
        # bgs = [BG, ...]
        # interp. a collection of 2 backgorunds to render next to each other, giving the effect of procedural landscaping
        self.bgs = [self.bg0, self.bg1]

        # TEMPLATE FOR BGS
        # for bg in bgs:
        #     ... bg
        pipeB0 = Game.Pipe_Bottom(3*self.SCREEN[0]//4,(self.SCREEN[1]//4) * 3)
        pipeT0 = Game.Pipe_Top(pipeB0.x,pipeB0.y - 350)
        # DD. PIPE_PAIR
        # pipePair = [PIPE_BOTTOM, PIPE_TOP]
        # interp. a pair of pipes that set the wall for the bird to pass through
        pipePair0 = [pipeB0,pipeT0]

        # TEMPLATE FOR PIPE_PAIR
        # for pipe in pipePair
        #   ... pipe
        self.pipes = [pipePair0]

        # Create 6 pairs of pipes
        for pp in range(6):
            self.addPipePair()

        # TEMPLATE FOR PIPES
        # for pipePair in pipes:
        #   for pipe in pipePair:
        #       ... pipe
    

    # DD. PIPES
    # pipes = [PIPE_PAIR, ...]
    # interp. a set of pipe pairs to render in the screen
    def addPipePair(self):
        pipePair = []
        lastBot = self.pipes[-1][0]
        offset = random.randint(-self.SCREEN[1]//4,self.SCREEN[1]//4)   #randomize the position of the bottom pipe
        # 1. create
        posY = (self.SCREEN[1]//4) * 3
        pipeB = Game.Pipe_Bottom(lastBot.x + int(3*lastBot.w), posY + offset) 
        # 2. append
        pipePair.append(pipeB)

        # 1. create
        pipeT = Game.Pipe_Top(pipeB.x,pipeB.y - 350)
        # 2. append
        pipePair.append(pipeT)

        # 3. append to pipes
        self.pipes.append(pipePair)

    def draw(self):
        self.display.fill("#1e1e1e")
        for bg in self.bgs:
            bg.draw(self.display)
        for pipePair in self.pipes:
            for ix,pipe in enumerate(pipePair):
                pipe.draw(self.display)
        self.fl0.draw(self.display)
        pygame.display.flip()

    def userInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and not Game.gameOver:
                self.fl0.jump = True

    def updateBGs(self):
        # if the right corner of the first bg in the list gets out of frame
        # get rid of it
        # create a new one at the right of the scene
        if self.bgs[0].x + self.bgs[0].w <=0:
            self.bgs.pop(0)
            # 1. create a new bg
            last_bg = self.bgs[-1]
            bg = Game.Bg(last_bg.x + last_bg.w, last_bg.y)
            # 2. append to the bgs
            self.bgs.append(bg)

        for bg in self.bgs:
            bg.x -= 3
        
    def updatePipes(self):

        # if the third pipe's pair in the system has left the screen on the left
        #   erase it and replace it for a new one at the end of the list
        firstPipeB = self.pipes[0][0]
        if firstPipeB.x + firstPipeB.w <=0:
            self.pipes.pop(0)
            # create a new pair of pipes and append them
            self.addPipePair()

        for pipePair in self.pipes:
            for pipe in pipePair:
                pipe.x -= 4

    def updateGameOver(self):
        for pipePair in self.pipes:
            for pipe in pipePair:
                if pipe.rect.colliderect(self.fl0.rect):
                    Game.gameOver = True

    def update(self):
        if not Game.gameOver:
            self.updateBGs()
            self.updatePipes()
            self.updateGameOver()
        self.userInput()

        

game = Game()
while True:
    game.draw()
    game.update()


# while True: draw(); update()