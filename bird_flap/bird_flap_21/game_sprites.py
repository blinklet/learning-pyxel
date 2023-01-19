import pyxel
import random
from sprite import Sprite


class Bird(Sprite):
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    SPRITE_SPEED = 1
    def __init__(self, x, y, animate_speed):
        Sprite.__init__(self, x, y, animate_speed)
        self.img = 0          # image bank number from resource file for bird animation
        self.u = 0            # initial bird horizontal position in image in resource file
        self.v = 16           # initial bird vertical position in image in resource file
        self.w = self.SPRITE_WIDTH    # bird width, used in Sprite superclass
        self.h = self.SPRITE_HEIGHT   # bird height, used in Sprite superclass
        self.col = 2          # sprite's transparent color
        self.start_sprite = random.randint(0,3)
        self.velocity_x = self.velocity_x * (self.SPRITE_SPEED / animate_speed) # each sprite starts with a randomly-selected velocity (direction)
        self.velocity_y = self.velocity_y * (self.SPRITE_SPEED / animate_speed)
        self.animate_clock = self.start_sprite
        self.frame = self.start_sprite
        self.sequence = [0, 1, 2, 1]
        self.animation_size = len(self.sequence)
        #self.animate_speed = animate_speed

    def move(self):
        # Choose next Bird in animation sequence. There are three bird frames
        # but we want to cycle back and forth across the frames so we want
        # the frame sequence to be: 0, 1, 2, 1, 0, 1, 2, 1, 0,...
        
        if self.animate_clock % self.animation_size == 0:
            self.frame = self.frame + 1
            self.animate_clock = self.animation_size
        if self.frame > self.animation_size -1:
            self.frame = 0
        self.u = 8 * self.sequence[self.frame]
        self.animate_clock = self.animate_clock - 1

        # set direction bird will face when moving
        self.facing = self.face()

        # move bird
        self.x += self.velocity_x
        self.y -= self.velocity_y
        # print("real x", self.real_x)
        # print("x", self.x)
        # print("real y", self.real_y)
        # print("y", self.y)
        # print()


class Ball(Sprite):
    SPRITE_WIDTH = 6
    SPRITE_HEIGHT = 6
    SPRITE_SPEED = 6
    def __init__(self, x, y, animate_speed):
        Sprite.__init__(self, x, y, animate_speed)
        self.img = 0          # image bank number from resource file for bird animation
        self.u = 17            # initial bird horizontal position in image in resource file
        self.v = 33           # initial bird vertical position in image in resource file
        self.w = self.SPRITE_WIDTH
        self.h = self.SPRITE_HEIGHT
        self.col = 2          # bird transparent color
        self.start_sprite = random.randint(0,1)
        self.velocity_x = self.velocity_x * (self.SPRITE_SPEED / animate_speed) # each sprite starts with a randomly-selected velocity (direction)
        self.velocity_y = self.velocity_y * (self.SPRITE_SPEED / animate_speed)
        self.animate_clock = self.start_sprite
        self.frame = self.start_sprite
        self.sequence = [0, 1]
        self.animation_size = len(self.sequence)
        #self.animate_speed = animate_speed

    def move(self):
        # Choose next ball in animation sequence. 
        # There are two ball frames
        if self.animate_clock % self.animation_size == 0:
            self.frame = self.frame + 1
            self.animate_clock = self.animation_size
        if self.frame > self.animation_size - 1:
            self.frame = 0

        self.u = 17 + 8 * self.sequence[self.frame]
        self.animate_clock = self.animate_clock - 1

        self.x += self.velocity_x
        self.y -= self.velocity_y

__all__ = ["Ball", "Bird"]
