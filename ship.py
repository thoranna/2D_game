from OpenGL.GL import *
from OpenGL.GLU import *

import math

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

class Ship:
    def __init__(self):
        self.r = 1
        self.b = 1
        self.g = 1

        self.x_pos = WINDOWWIDTH/2
        self.y_pos = WINDOWHEIGHT/2

        self.orbit_angle = 0

        self.speed = 1.3

        self.height = 40
        self.width = 5

    def display(self):

        glPushMatrix()
        glTranslate(self.x_pos, self.y_pos, 0)
        glRotate(self.orbit_angle*180/math.pi, 0, 0, 1)

        glBegin(GL_TRIANGLES)
        
        glColor3f(self.r, self.g, self.b)

        A = (-self.width, 0)
        B = (self.width, 0)
        C = (-self.width, self.height)
        D = (self.width, self.height)
        E = (0, self.height+25) # Top point
        F = (-self.width, self.height - 20) # Left wing
        G = (self.width, self.height - 20) # Right wing
        H = (-self.width-20, self.height-30) # Left wing
        I = (self.width + 20, self.height-30) # Right wing

        glVertex2f(*A)
        glVertex2f(*C)
        glVertex2f(*D)

        glVertex2f(*B)
        glVertex2f(*D)
        glVertex2f(*C)

        # TOPPUR - X 
        glVertex2f(*D)
        glVertex2f(*C)
        glVertex2f(*E)

        # VINSTRI HLIÐ
        glVertex2f(*C)
        glVertex2f(*F)
        glVertex2f(*H)

        # HÆGRI HLIÐ
        glVertex2f(*D)
        glVertex2f(*G)
        glVertex2f(*I)

        glEnd()

        glPopMatrix()
    
    def update(self, delta_time, left, right, up, down):
        if right:
            self.orbit_angle -= 0.01*delta_time
        if left:
            self.orbit_angle += 0.01*delta_time
        if up:
            self.x_pos += self.speed*delta_time*math.cos(math.pi/2 + self.orbit_angle)
            self.y_pos += self.speed*delta_time*math.sin(math.pi/2 + self.orbit_angle)
        if down:
            self.x_pos -= self.speed*delta_time*math.cos(math.pi/2 + self.orbit_angle)
            self.y_pos -= self.speed*delta_time*math.sin(math.pi/2 + self.orbit_angle)