"""
A simple 2D-Game, made for T-511-TGRA 
Author: Þóranna Dís Bender (thoranna18@ru.is)
"""
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from particle_system import Particle, Particles
from ball import MovingBall
from ship import Ship
from bullet import Bullet

import random
import math

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

class Game:
    def __init__(self, level=1):
        self.delta_time = 1
        self.clock = pygame.time.Clock()
        pygame.display.init()
        pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), DOUBLEBUF|OPENGL)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clock.tick()
        self.game_lost = False

        # ENABLE TRANSPARANCY
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.balls = []
        self.explosions = []
        self.bullets = []
        self.balls_to_delete = []
        self.bullets_to_delete = []
        self.balls_to_add = []
        self.ship = Ship(WINDOWWIDTH/2, WINDOWHEIGHT/2)
        self.left = 0
        self.right = 0
        self.up = 0 
        self.down = 0
        self.level = level
        self.positions = []

        if self.level == 1:
            self.positions = [(40, 40), 
                        (70, 150),
                        (160, 260),
                        (200, 60), 
                        (280, 380), 
                        (310, 100),
                        (370, 120), 
                        (400, 40), 
                        (630, 120),
                        (430, 90),
                        (460, 490),
                        (750, 500)]
        elif self.level == 2:
            self.positions = [(40, 40), 
                        (70, 150),
                        (160, 260),
                        (200, 60), 
                        (280, 380), 
                        (310, 100), 
                        (230, 160), 
                        (340, 220), 
                        (600, 60),
                        (540, 120),
                        (660, 490),
                        (710, 540),
                        (370, 120), 
                        (400, 40), 
                        (630, 120),
                        (430, 90)]
        elif self.level == 3:
            self.positions = [(40, 40), 
                        (70, 150),
                        (160, 260),
                        (200, 60), 
                        (280, 380), 
                        (310, 100), 
                        (230, 160), 
                        (340, 220), 
                        (600, 60),
                        (540, 120),
                        (660, 490),
                        (710, 540),
                        (370, 120), 
                        (400, 40), 
                        (630, 120),
                        (430, 90),
                        (460, 490),
                        (750, 500)]
        
        for t in self.positions:
            if self.level == 1:
                self.balls.append(MovingBall(*t))
            elif self.level == 2:
                b = MovingBall(*t)
                # b.speed = 0.4
                self.balls.append(b)
            elif self.level == 3:
                b = MovingBall(*t)
                # b.speed = 0.45
                self.balls.append(b)

    def game_loop(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == K_LEFT:
                    self.left = 1
                elif event.key == K_RIGHT:
                    self.right = 1
                elif event.key == K_UP:
                    self.up = 1
                elif event.key == K_DOWN:
                    self.down = 1
                if event.key == K_SPACE:
                    self.bullets.append(Bullet(self.ship.x_pos + math.cos(self.ship.orbit_angle+math.pi/2)*45, self.ship.y_pos + math.sin(self.ship.orbit_angle+math.pi/2)*45, self.ship.orbit_angle))
            elif event.type == pygame.KEYUP:
                if event.key == K_SPACE:
                    pass
                else:
                    self.left = 0
                    self.right = 0
                    self.up = 0 
                    self.down = 0

        # UPDATE LOGIC
        for i, b1 in enumerate(self.balls):
            if self.ship.calc_collision_w_bounding_box(b1):
                self.game_lost = True
            for j in range(i+1, len(self.balls)):
                b2 = self.balls[j]
                if b1.check_collision(b2):
                    if not ((b1.x_pos + b1.radius > WINDOWWIDTH or b1.x_pos - b1.radius < 0) or (b2.y_pos + b2.radius > WINDOWHEIGHT or b2.y_pos - b2.radius < 0)):
                        # BOUNCE
                        temp = b1.angle
                        b1.angle = b2.angle
                        b2.angle = temp

                        # NUDGE
                        # TODO: TAKE A BETTER LOOK AT THIS 
                        b1.x_pos += b1.speed*self.delta_time*math.cos(b1.angle)
                        b2.x_pos += b2.speed*self.delta_time*math.cos(b2.angle)
                        b1.y_pos += b1.speed*self.delta_time*math.sin(b1.angle)
                        b2.y_pos += b2.speed*self.delta_time*math.sin(b2.angle)

                        # SET COLLIDING BOOLEAN TO TRUE
                        b1.is_colliding = True
                        b2.is_colliding = True

                        # UPDATE BALLS
                        b1.update(self.delta_time)
                        b2.update(self.delta_time)

                        # APPEND PARTICLES TO EXPLOSIONS - upper bound on no of explosions
                        if len(self.explosions) <= 10:
                            particles = Particles(b1.x_pos+(b2.x_pos-b1.x_pos)/2, b1.y_pos+(b2.y_pos-b1.y_pos)/2)
                            ball = b1
                            for i, p in enumerate(particles.particle_list):
                                if i >= len(particles.particle_list)/2:
                                    ball = b2
                                p.r, p.g, p.b = ball.r, ball.g, ball.b

                            self.explosions.append(particles)
            
            if not b1.is_colliding:
                b1.update(self.delta_time)
        
        # BULLET COLLISION LOGIC
        self.balls_to_delete = []
        self.bullets_to_delete = []
        self.balls_to_add = []
        for i, b1 in enumerate(self.balls):
            for j, bullet in enumerate(self.bullets):
                if self.check_collision(b1, bullet):
                    if b1.radius <= 13.5:
                        particles = Particles(b1.x_pos, b1.y_pos)
                        for p in particles.particle_list:
                            p.r, p.b, p.g = b1.r, b1.b, b1.g
                            p.decay = 1
                        self.explosions.append(particles)
                    else:
                        if not ((b1.x_pos + b1.radius/2 > WINDOWWIDTH or b1.x_pos - b1.radius/2 < 0) or (b1.y_pos + b1.radius/2 > WINDOWHEIGHT or b1.y_pos - b1.radius/2 < 0)):
                            smaller_ball1 = MovingBall(b1.x_pos + b1.radius/2, b1.y_pos + b1.radius/2, b1.radius/2)
                            smaller_ball2 = MovingBall(b1.x_pos - b1.radius/2, b1.y_pos - b1.radius/2, b1.radius/2)
                        else:
                            # TODO: TAKE A BETTER LOOK AT THIS LOGIC 
                            if b1.x_pos + b1.radius/2 > WINDOWWIDTH:
                                smaller_ball1 = MovingBall(b1.x_pos - b1.radius/2, b1.y_pos + b1.radius/2, b1.radius/2)
                                smaller_ball1 = MovingBall(b1.x_pos - b1.radius/2, b1.y_pos + b1.radius/2, b1.radius/2)
                            elif b1.x_pos - b1.radius/2 < 0:
                                smaller_ball1 = MovingBall(b1.x_pos + b1.radius/2, b1.y_pos + b1.radius/2, b1.radius/2)
                                smaller_ball1 = MovingBall(b1.x_pos + b1.radius/2, b1.y_pos + b1.radius/2, b1.radius/2)
                            elif b1.y_pos + b1.radius/2 > WINDOWHEIGHT:
                                smaller_ball1 = MovingBall(b1.x_pos + b1.radius/2, b1.y_pos - b1.radius/2, b1.radius/2)
                                smaller_ball1 = MovingBall(b1.x_pos + b1.radius/2, b1.y_pos - b1.radius/2, b1.radius/2)
                            elif b1.y_pos - b1.radius/2 < 0:
                                smaller_ball1 = MovingBall(b1.x_pos + b1.radius/2, b1.y_pos + b1.radius/2, b1.radius/2)
                                smaller_ball1 = MovingBall(b1.x_pos + b1.radius/2, b1.y_pos + b1.radius/2, b1.radius/2)
                        
                        smaller_ball1.r, smaller_ball1.b, smaller_ball1.g = b1.r, b1.b, b1.g
                        smaller_ball2.r, smaller_ball2.b, smaller_ball2.g = b1.r, b1.b, b1.g
                                
                        self.balls_to_add.append(smaller_ball1)
                        self.balls_to_add.append(smaller_ball2)
                        self.bullets_to_delete.append(j)
                    
                    self.balls_to_delete.append(i)
    
    def update(self):

        for i in self.balls_to_delete[::-1]:
            self.balls.pop(i)

        for i in self.bullets_to_delete[::-1]:
            self.bullets.pop(i)
        
        for ball in self.balls_to_add:
            self.balls.append(ball)

        explosions_to_delete = []
        for i, explosion in enumerate(self.explosions):
            if len(explosion.particle_list) == 0:
                explosions_to_delete.append(i)
            explosion.update()
        
        for i in explosions_to_delete[::-1]:
            self.explosions.pop(i)
        
        self.delta_time = self.clock.tick()/5.0
        self.ship.update(self.delta_time, self.right, self.left, self.up, self.down)
        for bullet in self.bullets:
            bullet.update(self.delta_time)

    def display(self):
        # DISPLAY
        glClear(GL_COLOR_BUFFER_BIT)
            
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(0, 0, WINDOWWIDTH, WINDOWHEIGHT)
        gluOrtho2D(0, WINDOWWIDTH, 0, WINDOWHEIGHT)

        self.ship.display()
        for bullet in self.bullets:
            bullet.display()

        for b in self.balls:
            b.display()

        for i, explosion in enumerate(self.explosions):
            explosion.display()
        
        pygame.display.flip()


if __name__ == "__main__":

    game = Game()
    while True:
        game.game_loop()
        game.update()
        game.display()
        if len(game.balls) == 0: # If you win a level
            if game.level == 3: # If you win the last level
                for t in game.positions:
                    particles = Particles(*t)
                    for p in particles.particle_list:
                        p.r, p.b, p.g = random.random(), random.random(), random.random()
                        p.decay = 1
                    game.explosions.append(particles)
                for _ in range(100):
                    game.game_loop()
                    game.update()
                    game.display()
                pass
            game.level += 1
            game = Game(level)
        if game.game_lost: # If you loose
            game.ship.able_to_move = False
            for b in game.balls:
                b.able_to_move = False
            const = -1
            for _ in range(100):
                game.game_loop()
                game.ship.decay = const
                game.update()
                game.display()
                const = -const
            game.ship.decay = 0
            particles = Particles(game.ship.x_pos, game.ship.y_pos, 100)
            for p in particles.particle_list:
                p.decay_rate = 0.005
            game.explosions.append(particles)
            for _ in range(600):
                game.game_loop()
                game.update()
                game.display()
            game = Game()