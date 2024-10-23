import pygame
import random 



DIMS = (40,30)
RES = 16
SCREEN = (DIMS[0]*RES, DIMS[1]*RES)
display = pygame.display.set_mode(SCREEN)

# DD. DIRECTION
# DIRECTION = [int,int,int,int]
# interp. the 4 cardinal directions, encoded by name
RIGHT = [1,0,0,0]
DOWN = [0,1,0,0]
LEFT = [0,0,1,0]
UP = [0,0,0,1]

GAMEOVER_PENALTY = -10
FOOD_REWARD = 10
IDLE_PENALTY = -10
FPS = 40
