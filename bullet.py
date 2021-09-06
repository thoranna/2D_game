from OpenGL.GL import *
from OpenGL.GLU import *

import math

class Bullet:
    def __init__(self, x_pos, y_pos, angle):
        self.r = 1
        self.b = 1
        self.g = 1

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.speed = 3
        self.radius = 3

        self.angle = angle
    
    def display(self):
        glBegin(GL_TRIANGLE_FAN) # BEGIN CIRCLE 
        glColor3f(self.r, self.g, self.b) # SET COLOR
        glVertex2f(self.x_pos, self.y_pos) # DEFINE STARTING POS
        twice_pi = 2.5*3.142
        n_iter = 30

        for i in range(n_iter):
            glVertex2f(self.x_pos + (self.radius*math.cos(i*twice_pi/n_iter)), self.y_pos + (self.radius*math.sin(i*twice_pi/n_iter)))
            glColor3f(self.r, self.g, self.b)
        glEnd()

    def update(self, delta_time):
        self.x_pos += self.speed*delta_time*math.cos(math.pi/2 + self.angle)
        self.y_pos += self.speed*delta_time*math.sin(math.pi/2 + self.angle)

