from ursina import *


class Bullet():
    def __init__(self, x, y, direction, gravity=0.01, speed=20, paint=(150,50,50), measures=(.7,.3,.1)):
        if direction == 0:
            y += 1
            
        self.entity = Entity(
                model = 'cube',
                color = color.rgb(paint[0],paint[1],paint[2]),
                x = x,
                y = y,
                scale = (measures[0],measures[1],measures[2]),
                collider = 'box')
        self.direction = direction
        self.initial_gravity = gravity
        self.gravity = gravity
        self.speed = speed
        self.hits = 2

        
    def move(self):
        self.entity.x += time.dt * self.speed * self.direction
        if self.direction == 0:
            self.entity.y += time.dt * self.speed/2
        self.gravity *= 1.03
        self.entity.y -= self.gravity

    

