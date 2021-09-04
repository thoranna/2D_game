import random
import math

from OpenGL.GL import *
from OpenGL.GLU import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

class MovingBall:
    def __init__(self, x_pos, y_pos):

        self.x_pos = x_pos
        self.y_pos = WINDOWHEIGHT - y_pos
        self.radius = 27

        self.x_change = 0.5 if random.random() < 0.5 else -0.5
        self.y_change = 0.5 if random.random() < 0.5 else -0.5

        self.r = random.random()
        self.g = random.random()
        self.b = random.random()

        self.is_colliding = False

    def update(self):

        self.x_pos += self.x_change
        self.y_pos += self.y_change
        if self.y_pos + self.radius > WINDOWHEIGHT or self.y_pos - self.radius < 0:
            self.y_change = self.y_change * -1
            if self.y_pos + self.radius > WINDOWHEIGHT:
                self.y_pos -= 0.5
            else:
                self.y_pos += 0.5
            self.r = random.random()
            self.g = random.random()
            self.b = random.random()
        if self.x_pos + self.radius > WINDOWWIDTH or self.x_pos - self.radius < 0:
            self.x_change = self.x_change * -1
            if self.x_pos + self.radius > WINDOWWIDTH:
                self.x_pos -= 0.5
            else:
                self.x_pos += 0.5
            self.r = random.random()
            self.g = random.random()
            self.b = random.random()
        
        # Change color on collision
        if self.is_colliding:
            self.r = random.random()
            self.g = random.random()
            self.b = random.random()
            self.is_colliding = False
    
    def display(self):

        glBegin(GL_TRIANGLE_FAN) # BEGIN CIRCLE 
        glColor3f(self.r, self.g, self.b) # SET COLOR
        glVertex2f(self.x_pos, self.y_pos) # DEFINE STARTING POS
        twice_pi = 2.5*3.142
        n_iter = 30

        for i in range(n_iter):
            glVertex2f(self.x_pos + (self.radius*math.cos(i*twice_pi/n_iter)), self.y_pos + (self.radius*math.sin(i*twice_pi/n_iter)))
            glColor3f(self.r*0.45, self.g*0.45, self.b*0.45)
        glEnd()