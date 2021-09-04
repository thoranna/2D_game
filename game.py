"""
    2D-Game
    Author: Þóranna Dís Bender (thoranna18@ru.is)
"""

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from particle_system import Particle, Particles
from ball import MovingBall, WINDOWHEIGHT, WINDOWWIDTH

import random
import math

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
    
    # INITIALIZE MOVING BALLS
    balls = []
    explosions = []

    positions = [(100, 200), 
                (160, 260),
                (220, 320), 
                (280, 380), 
                (340, 440),
                (400, 500), 
                (200, 100), 
                (260, 160), 
                (320, 220), 
                (440, 340), 
                (500, 400), 
                (600, 60), 
                (660, 560)]
    
    for t in positions:
        balls.append(MovingBall(*t))

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
                    balls.append(MovingBall(x_pos, y_pos))
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
        for i, b1 in enumerate(balls):
            for j in range(i+1, len(balls)):
                b2 = balls[j]
                if check_collision(b1, b2):
                    if not ((b1.x_pos + b1.radius > WINDOWWIDTH or b1.x_pos - b1.radius < 0) or (b2.y_pos + b2.radius > WINDOWHEIGHT or b2.y_pos - b2.radius < 0)):
                        b1.x_change = b1.x_change*-1
                        b1.y_change = b1.y_change*-1
                        b2.x_change = b2.x_change*-1
                        b2.y_change = b2.y_change*-1

                        # NUDGE
                        b1.x_pos += b1.x_change*10
                        b2.x_pos += b2.x_change*10
                        b1.y_pos += b1.y_change*10
                        b2.y_pos += b2.y_change*10
 
                        b1.is_colliding = True
                        b2.is_colliding = True

                        b1.update()
                        b2.update()

                        explosions.append(Particles(b1.x_pos+(b2.x_pos-b1.x_pos)/2, b1.y_pos+(b2.y_pos-b1.y_pos)/2))
        
            if not b1.is_colliding:
                b1.update()

        explosions_to_delete = []
        for i, explosion in enumerate(explosions):
            if len(explosion.particle_list) == 0:
                explosions_to_delete.append(i)
            explosion.update()
        
        for i in explosions_to_delete[::-1]:
            explosions.pop(i)
        
        # DISPLAY
        glClear(GL_COLOR_BUFFER_BIT)
            
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(0, 0, WINDOWWIDTH, WINDOWHEIGHT)
        gluOrtho2D(0, WINDOWWIDTH, 0, WINDOWHEIGHT)
        
        for b in balls:
            b.display()

        for i, explosion in enumerate(explosions):
            explosion.display()
        
        pygame.display.flip()