import random
import math

from OpenGL.GL import *
from OpenGL.GLU import *

class Particle:
    def __init__(self, x_pos, y_pos):
        self.radius = 2.5

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.x_change = 2*random.random() - 1
        self.y_change = 2*random.random() - 1

        self.r = 1
        self.g = 1
        self.b = 1

        self.decay = random.random()*0.5 + 0.5

    def update(self):
        self.x_pos += self.x_change
        self.y_pos += self.y_change
        self.decay -= 0.01
    
    def display(self):
        
        glEnable(GL_BLEND) # ENABLE TRANSPARANCY 
        glBegin(GL_TRIANGLE_FAN)
        glColor4f(self.r, self.g, self.b, self.decay)
        glVertex2f(self.x_pos, self.y_pos)
        
        twice_pi = 2.5*3.142
        n_iter = 10

        for i in range(n_iter):
            glVertex2f(self.x_pos + (self.radius*math.cos(i*twice_pi/n_iter)), self.y_pos + (self.radius*math.sin(i*twice_pi/n_iter)))
            glColor4f(self.r, self.g, self.b, self.decay)
        
        glEnd()

class Particles:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.particle_list = []
        self.initialize_particles()

    def initialize_particles(self):
        
        for _ in range(20):
            p = Particle(self.x_pos, self.y_pos)
            self.particle_list.append(p)
    
    def update(self):

        particles_to_delete = []
        for i, particle in enumerate(self.particle_list):
            if particle.decay >= 0:
                particle.update()
            else:
                particles_to_delete.append(i)

        for i in particles_to_delete[::-1]:
            self.particle_list.pop(i)
    
    def display(self):
        for particle in self.particle_list:
            particle.display()