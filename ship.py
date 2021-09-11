from OpenGL.GL import *
from OpenGL.GLU import *

import math

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
    
class Ship:
    def __init__(self, x_pos, y_pos):
        self.r = 1
        self.b = 1
        self.g = 1

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.orbit_angle = 0

        self.speed = 1.3

        self.height = 20
        self.width = 5

        self.decay = 1

        self.able_to_move = True

        self.bounding_box_height = 40
        self.bounding_box_width = 64

    def display(self):

        glPushMatrix()
        glTranslate(self.x_pos, self.y_pos, 0)
        glRotate(self.orbit_angle*180/math.pi, 0, 0, 1)
        glBegin(GL_TRIANGLES)
        glColor4f(self.r, self.g, self.b, self.decay)

        # Body of the ship 
        A = (-self.width, -self.height)
        B = (self.width, -self.height)
        C = (-self.width, self.height)
        D = (self.width, self.height)
        E = (0, self.height+25) # Top point
        F = (-self.width, self.height - 20) # Left wing
        G = (self.width, self.height - 20) # Right wing
        H = (-self.width-20, self.height-30) # Left wing
        I = (self.width + 20, self.height-30) # Right wing

        # BODY 
        glVertex2f(*A)
        glVertex2f(*C)
        glVertex2f(*D)

        glVertex2f(*B)
        glVertex2f(*D)
        glVertex2f(*C)

        # TOP
        glVertex2f(*D)
        glVertex2f(*C)
        glVertex2f(*E)

        # LEFT SIDE
        glVertex2f(*C)
        glVertex2f(*F)
        glVertex2f(*H)

        # RIGHT SIDE
        glVertex2f(*D)
        glVertex2f(*G)
        glVertex2f(*I)

        glEnd()

        glPopMatrix()

    def clamp(self, val, min_, max_):
        return max(min_, min(max_, val))
    
    def calc_collision_w_bounding_box(self, ball_object):
        # Step 1: Get the center point
        center = (ball_object.x_pos, ball_object.y_pos)
        # Step 2: Calculate AABB info (center, half-extents)*m
        aabb_half_extents = (self.bounding_box_width/2.0, self.bounding_box_height/2.0)
        aabb_center = (self.x_pos + aabb_half_extents[0], self.y_pos + aabb_half_extents[1])
        # Step 3: Get the difference vector between both centers
        diff_vec = (center[0]-aabb_center[0], center[1]-aabb_center[1])
        clamped = (self.clamp(diff_vec[0], -aabb_half_extents[0], aabb_half_extents[0]), self.clamp(diff_vec[1], -aabb_half_extents[1], aabb_half_extents[1]))
        # Step 4: Add clamped value to the AABB center and get the value of box closest to the circle
        closest = (aabb_center[0] + clamped[0], aabb_center[1] + clamped[1])
        difference = (closest[0] - center[0], closest[1] - center[1])
        return math.sqrt(difference[0]**2+difference[1]**2) <= ball_object.radius
    
    def update(self, delta_time, left, right, up, down):
        if not self.able_to_move:
            pass
        else:
            if left:
                self.orbit_angle -= 0.01*delta_time
            if right:
                self.orbit_angle += 0.01*delta_time
            if up:
                self.x_pos += self.speed*delta_time*math.cos(math.pi/2 + self.orbit_angle)
                self.y_pos += self.speed*delta_time*math.sin(math.pi/2 + self.orbit_angle)
            if down:
                self.x_pos -= self.speed*delta_time*math.cos(math.pi/2 + self.orbit_angle)
                self.y_pos -= self.speed*delta_time*math.sin(math.pi/2 + self.orbit_angle)