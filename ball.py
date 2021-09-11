import random
import math

from OpenGL.GL import *
from OpenGL.GLU import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

class MovingBall:
    def __init__(self, x_pos, y_pos, radius = 27):

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius 

        self.speed = 0.35
        self.angle = 2*3.1415*random.random()
        
        self.r = random.random()
        self.g = random.random()
        self.b = random.random()

        self.is_colliding = False
        self.able_to_move = True 

    def update(self, delta_time):

        if self.able_to_move:
            self.x_pos += self.speed*delta_time*math.cos(self.angle)
            self.y_pos += self.speed*delta_time*math.sin(self.angle)
            if (self.y_pos + self.radius > WINDOWHEIGHT or self.y_pos - self.radius < 0) or (self.x_pos + self.radius > WINDOWWIDTH or self.x_pos - self.radius < 0):
                if self.y_pos + self.radius > WINDOWHEIGHT or self.y_pos - self.radius < 0:
                    self.angle = -self.angle
                else:
                    self.angle = math.pi - self.angle

                if self.y_pos + self.radius > WINDOWHEIGHT:
                    self.y_pos = WINDOWHEIGHT - self.radius
                elif self.y_pos - self.radius < 0:
                    self.y_pos = self.radius
                if self.x_pos + self.radius > WINDOWWIDTH:
                    self.x_pos = WINDOWWIDTH - self.radius
                elif self.x_pos - self.radius < 0:
                    self.x_pos = self.radius
                
                self.r = random.random()
                self.g = random.random()
                self.b = random.random()
            
            # Change color on collision
            if self.is_colliding:
                self.r = random.random()
                self.g = random.random()
                self.b = random.random()
                self.is_colliding = False
        else:
            pass
    
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