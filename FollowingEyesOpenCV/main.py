''' 
OpenYourEyes is a program that uses the user's webcam to perceive movement, then combines it with pygame to 
render eyes that follow the biggest source of movement across the room
'''

import pygame
import cv2
from objectDetection import *
from circleVect import *
import numpy as np


# DATA DEFS
SCREEN = (500,500)
RES = 128
distance = 20          #the distance between the two eyes
display = pygame.display.set_mode(SCREEN, pygame.RESIZABLE)
FPS = 30

# DD. EYE
# eye = Eye()
# interp. an eye that follow the user across the screen

class Eye():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # A set of coordinates for the pupils
        self.xPup = x
        self.yPup = y
        # update and create the rect component
        self.updateRect()
        self.dx = 0
        self.dy = 0

    def updateRect(self):
        self.eyeBall = pygame.image.load(f"./images/res_{RES}/{RES}_1.png")
        self.rectEB = self.eyeBall.get_rect()
        self.rectEB.center = self.x, self.y

        self.pupil = pygame.image.load(f"./images/res_{RES}/{RES}_0.png")
        self.rectPup = self.pupil.get_rect()
        self.rectPup.center = self.xPup, self.yPup
    
    def draw(self):
        display.blit(self.eyeBall,self.rectEB)
        display.blit(self.pupil,self.rectPup)

    def updateDir(self):
        # self.xPup += self.dx * 20
        # self.yPup += self.dy * 20
        # self.rectPup.center = self.xPup, self.yPup
        self.xPup = self.x + self.dx
        self.yPup = self.y + self.dy
        self.rectPup.center = self.xPup, self.yPup

eyeL = Eye((SCREEN[0]//2) - ((RES//2) + distance),(SCREEN[1]//2) - 130)
eyeR = Eye((SCREEN[0]//2) + ((RES//2) + distance),(SCREEN[1]//2) - 130)

# DD. FACE
# face = pygame.image.load("./images/main.png")
# interp. the face of the character in the scene
class Face():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.updateRect()
    
    def updateRect(self):
        self.image = pygame.image.load(f"./images/res_{RES}/{RES}_main.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
    
    def draw(self):
        display.blit(self.image, self.rect)


face = Face(SCREEN[0]//2, SCREEN[1]//2)




# cap = cv2.VideoCapture(0)
####################### CODING SECTION ###################

def draw():
    display.fill("#1e1e1e")
    # frame= np.rot90(cap.read()[1])
    # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # frame=pygame.surfarray.make_surface(frame)
    # display.blit(frame,(0,0))
    eyeL.draw()
    eyeR.draw()
    face.draw()
    pygame.display.flip()

def userInput():
    global display
    global SCREEN
    events = pygame.event.get()
    for event in events:
        
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.VIDEORESIZE:
            SCREEN = (event.w, event.h)
            display = pygame.display.set_mode(SCREEN,pygame.RESIZABLE)
            eyeL.x =(SCREEN[0]//2) - ((RES//2) + distance) - 40
            eyeR.x =(SCREEN[0]//2) + ((RES//2) + distance) - 40
            eyeL.y =(SCREEN[1]//2) - 130
            eyeR.y =(SCREEN[1]//2) - 130
            face.x = SCREEN[0]//2
            face.y = SCREEN[1]//2
            eyeL.updateRect()
            eyeR.updateRect()
            face.updateRect()

def update():
    userInput()
    
    cameraPos = readCamera(SCREEN[0],SCREEN[1])
    if cameraPos != None:
        # Get the direction of the eyes' movement
        eyeL.dx, eyeL.dy = getPosXY((eyeL.x, eyeL.y),cameraPos, SCREEN, (eyeL.x, eyeL.y))
        eyeR.dx, eyeR.dy = eyeL.dx, eyeL.dy
    # # invert the value of dx to give a mirror like effect
    # Apply the direction to the eyes
    eyeL.updateDir()
    eyeR.updateDir()



    


# CODING SECTION


while True:
    draw()
    update()