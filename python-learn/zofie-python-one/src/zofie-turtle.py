#!/usr/bin/env python3

import colorsys
import random
import sys
import turtle
from turtle import *


shape("turtle")
speed(9900)
pencolor("white")
pensize(6)
Screen().bgcolor("turquoise")

def vshape():
    right(25)
    forward(50)
    backward(50)
    left(50)
    forward(50)
    backward(50)
    right(25)

def snowflakeArm():
    for x in range(0,4):
        forward(30)
        vshape()
    backward(120)

def snowflake():
    for x in range(0, 60):
        pencolor(["white", "red", "blue", "green", "yellow", "purple", "cyan", "plum", "goldenrod"][random.randint(0, 8)])
        #pencolor(x / 90.0, x /  90.0, x / 90.0)
        pencolor(random.random(), random.random(), random.random())
        pencolor(colorsys.hsv_to_rgb(x/60.0, 1.0, 1.0))
        snowflakeArm()
        right(6)

snowflake()

turtle.onscreenclick(lambda x, y: sys.exit(0), 1)
turtle.mainloop()
