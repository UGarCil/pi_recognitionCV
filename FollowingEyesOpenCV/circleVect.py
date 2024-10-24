################ MODULES
''' Calculate the rate of change in X and Y given the distance between two points'''

import pygame
import math
from math import degrees as degrees
from math import atan2 as atan
################### DATA DEFS



####################### CODE
# FD. remap()
# Signature: float, float, float, float, float -> float
# purp. rescale a given value
def remap(value, from1, to1, from2, to2):
    return (value - from1) / (to1 - from1) * (to2 - from2) + from2

def hip(pointA,pointB):
    a = pointB[0] - pointA[0]
    b = pointB[1] - pointA[1]
    return (math.sqrt((a**2) + (b**2)))

def getPosXY(circleCenter, targetPos,SCREEN, EYECENTER):
    RADIUS = int(remap(hip(circleCenter, targetPos), 0,SCREEN[0],0,90))

    # Calculate the tangent (ratio of opposite vs. adjacent)
    o =  circleCenter[1] - targetPos[1]
    a =  circleCenter[0] - targetPos[0]

    # Calculate the value of tan when divisor == 0 exist
    tan = o/a if a != 0 else 0
    angle = float(math.atan(tan))

    
    # Default value for the 0 divisors
    # adjascent has no value and opposite side bigger than 0
    if abs(a) == 0.0 and o > 0:
        angle = (6.28/4) * 3
    # adjascent has not value and opposite side less than 0
    if abs(a) == 0.0 and o < 0:
        angle = (6.28/4) * 1
    # opposite side has not value and adjascent side more than 0
    if abs(o) == 0.0 and a > 0:
        # angle = (6.28/4) * 2
        pass
        # print("Here")
    # opposite side has not value and adjascent side less than 0
    if abs(o) == 0.0 and a < 0:
        # angle = (6.28/4) * 0
        pass

    # # If the pointer is below the center of the circle in the x axis, a is positive.
    # Invert the angle to reflect the circle and add pi to the calculation of x
    if a > 0:
        angle = -angle
        x = RADIUS * math.cos(angle + (6.28/2))
        y = RADIUS * math.sin(angle)
    
    else:
        x = RADIUS * math.cos(angle)
        y = RADIUS * math.sin(angle)
    
    return(x,y)
    
