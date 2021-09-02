"""
    Simple shapes and motions for T-511-TGRA Assignment 1
    Author: Þóranna Dís Bender (thoranna18@ru.is)
"""

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random
import math

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

LEFT = 0
RIGHT = 0
UP = 0
DOWN = 0

class MovingObject:
    def __init__(self, x_pos, y_pos, id):

        self.x_pos = x_pos
        self.y_pos = WINDOWHEIGHT - y_pos
        self.radius = 25
        self.id = id

        self.x_change = 0.7 if random.random() < 0.7 else -0.7
        self.y_change = 0.7 if random.random() < 0.7 else -0.7

        self.r = 0.0
        self.g = 1.0
        self.b = 0.0

        self.is_colliding = False

    def update(self):

        if LEFT:
            if self.x_pos - self.radius*2 <= 0:
                pass
            else:
                self.x_pos -= 0.5
        if RIGHT:
            if self.x_pos + self.radius*2 >= WINDOWWIDTH:
                pass
            else:
                self.x_pos += 0.5
        if DOWN:
            if self.y_pos - self.radius*2 <= 0:
                pass
            else:
                self.y_pos -= 0.5
        if UP:
            if self.y_pos + self.radius*2 >= WINDOWHEIGHT:
                pass
            else:
                self.y_pos += 0.5
        if not RIGHT and not LEFT and not DOWN and not UP:
            self.x_pos += self.x_change
            self.y_pos += self.y_change
            if self.y_pos + self.radius > WINDOWHEIGHT or self.y_pos - self.radius < 0:
                self.y_change = self.y_change * -1
                self.r = random.random()
                self.g = random.random()
                self.b = random.random()
            if self.x_pos + self.radius > WINDOWWIDTH or self.x_pos - self.radius < 0:
                self.x_change = self.x_change * -1
                self.r = random.random()
                self.g = random.random()
                self.b = random.random()
        
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
        off = 0.45
        m_range = 30

        for i in range(m_range):
            glVertex2f(self.x_pos + (self.radius*math.cos(i*twice_pi/m_range)), self.y_pos + (self.radius*math.sin(i*twice_pi/m_range)))
            glColor3f(self.r*off, self.g*off, self.b*off)
        glEnd()

def check_collision(game_object1, game_object2):
    d = math.sqrt(((game_object2.x_pos - game_object1.x_pos)**2+(game_object2.y_pos - game_object1.y_pos)**2))
    if d <= game_object1.radius*2:
        return True
    return False

def calc_change(game_object1, game_object2):
    pass


if __name__ == "__main__":

    # INITIAL DISPLAY
    pygame.display.init()
    pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), DOUBLEBUF|OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    acc_id = 2
    b1 = MovingObject(300, 400, 0)
    b2 = MovingObject(400, 500, 1)
    boxes = [b1, b2]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == K_LEFT:
                    LEFT = 1
                elif event.key == K_RIGHT:
                    RIGHT = 1
                elif event.key == K_UP:
                    UP = 1
                elif event.key == K_DOWN:
                    DOWN = 1
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1:
                    x_pos = pygame.mouse.get_pos()[0]
                    y_pos = pygame.mouse.get_pos()[1]
                    if y_pos + b.radius > WINDOWHEIGHT:
                        y_pos = WINDOWHEIGHT - b.radius
                    elif y_pos - b.radius < 0:
                        y_pos = b.radius
                    if x_pos + b.radius > WINDOWWIDTH:
                        x_pos = WINDOWWIDTH - b.radius
                    elif x_pos - b.radius < 0:
                        x_pos = b.radius
                    boxes.append(MovingObject(x_pos, y_pos, acc_id))
                    acc_id += 1
            elif event.type == pygame.KEYUP:
                if event.key == K_LEFT:
                    LEFT = 0
                elif event.key == K_RIGHT:
                    RIGHT = 0
                elif event.key == K_DOWN:
                    DOWN = 0
                elif event.key == K_UP:
                    UP = 0

        # UPDATE LOGIC
        for box1 in boxes:
            for box2 in boxes:
                if box1.id != box2.id:
                    if check_collision(box1, box2):
                        box1.x_change = box1.x_change*-1
                        box1.x_pos += box1.x_change
                        box2.y_change = box2.y_change*-1
                        box2.y_pos += box2.y_change
                        box1.is_collding = True
                        box2.is_colliding = True
            box1.update()
        
        # DISPLAY
        glClear(GL_COLOR_BUFFER_BIT)
            
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(0, 0, WINDOWWIDTH, WINDOWHEIGHT)
        gluOrtho2D(0, WINDOWWIDTH, 0, WINDOWHEIGHT)
        for b in boxes:
            b.display()
        pygame.display.flip()