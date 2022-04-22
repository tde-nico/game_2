from ursina import *
from modules import Bullet


class Player():
    def __init__(self, x, y, fov=30, paint=(255,0,0), measures=(2, 2, 1)):
        self.entity = Entity(
            model = 'cube',
            color = color.rgb(paint[0],paint[1],paint[2]),
            x = x,
            y = y,
            scale = (measures[0], measures[1], measures[2]),
            collider = 'box')

        self.fov = fov

        self.speed = 0.3
        self.orientation = 0

        self.ground = False
        self.gravity = 0.01
        self.initial_gravity = self.gravity
        self.fall_coefficent = 1.2

        self.jump = False
        self.max_jumps = 2
        self.jump_left = self.max_jumps
        self.jump_delay = True
        
        self.left_dashes = 1
        
        self.left_bullets = 1
        
        self.in_respawn = False
        self.respawn_time = 2
           


    def move(self, right, left, up):
        self.entity.x += right * self.speed
        self.entity.x -= left * self.speed
        if right > left:
            self.orientation = 1
        elif right < left:
            self.orientation = -1
        else:
            self.orientation = 0
        
        if up and self.jump_left > 0 and self.jump_delay:
            self.jump = True
            self.gravity = 1.5
            self.jump_left -= 1
            self.jump_delay = False
            invoke(setattr, self, 'jump_delay', True, delay=.3)
        if self.jump:
            self.gravity /= self.fall_coefficent
            self.entity.y += self.gravity
            if self.gravity < .01:
                self.gravity = self.initial_gravity
                self.jump = False
        elif not self.ground:
            if self.gravity <= .7:
                self.gravity *= self.fall_coefficent
            self.entity.y -= self.gravity
        else:
            self.entity.y = self.ground.y + self.ground.scale_y/2 + self.entity.scale_y/2
            self.gravity = self.initial_gravity
            self.jump_left = self.max_jumps
            

    def dash(self):
        self.entity.x += self.orientation * 3
        self.left_dashes -=1
        invoke(setattr, self, 'left_dashes', 1, delay=1)


    def respawn(self, hitted=False):
        if (not self.in_respawn and ((self.entity.y < (-self.fov/2 -3)) or (self.entity.x > (self.fov + 1)) or (self.entity.x < (-self.fov + 1)))) or hitted:
            self.entity.y = -self.fov
            invoke(setattr, self, 'in_respawn', False, delay=self.respawn_time+.5)
            invoke(setattr, self.entity, 'x', 0, delay=self.respawn_time)
            invoke(setattr, self.entity, 'y', 0, delay=self.respawn_time)
            invoke(setattr, self, 'gravity', self.initial_gravity, delay=self.respawn_time)
            self.in_respawn = True
            


    def shoot(self):
        self.left_bullets -=1
        invoke(setattr, self, 'left_bullets', 1, delay=1)
        x = self.entity.x+self.orientation*2
        y = self.entity.y+1
        paint = (150,50,50)
        measures = (.7,.3,.1)
        return Bullet.Bullet(x, y, self.orientation, 0.01, 20, paint, measures) ,(x, y, measures, paint)


