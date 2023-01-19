import random
from sprite import Sprite
import math


class Bird(Sprite):
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    SPRITE_SPEED = 1
    SPRITE_FPS = 3            # animation frame rate
    def __init__(self, x, y, fastest_sprite_speed, game_fps):
        Sprite.__init__(self, x, y, fastest_sprite_speed, game_fps)
        self.img = 0          # image bank number from resource file for bird animation
        self.u = 0            # initial bird horizontal position in image in resource file
        self.v = 16           # initial bird vertical position in image in resource file
        self.w = self.SPRITE_WIDTH            # bird width
        self.h = self.SPRITE_HEIGHT           # bird height
        self.col = 2          # bird transparent color
        self.frame = random.randint(0,3)
        self.sequence = [0, 1, 2, 1]
        self.animation_size = len(self.sequence)

        # each sprite starts with a randomly-selected velocity (direction)
        self.velocity_x = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
        self.velocity_y = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
        
        # avoid motionless sprites
        while self.velocity_x == 0 and self.velocity_y == 0:
            print('Motionless sprite. Resetting velocity')
            self.velocity_x = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
            self.velocity_y = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
            

    def move(self):
        # Choose next Bird in animation sequence. There are three bird frames
        # but we want to cycle back and forth across the frames so we want
        # the frame sequence to be: 0, 1, 2, 1, 0, 1, 2, 1, 0,...
        
        if self.animate_clock % math.ceil((self.game_fps * self.fastest_sprite_speed)//self.SPRITE_FPS) == 0:
            self.frame = self.frame + 1
        if self.frame > self.animation_size -1:
            self.frame = 0
        self.u = 8 * self.sequence[self.frame]
        self.animate_clock = self.animate_clock + 1
        print(self.frame, self.sequence[self.frame])

        # set direction bird will face when moving
        self.facing = self.face()

        # move bird
        self.x += self.velocity_x
        self.y -= self.velocity_y


class Ball(Sprite):
    SPRITE_WIDTH = 6
    SPRITE_HEIGHT = 6
    SPRITE_SPEED = 2
    SPRITE_FPS = 2            # animation frame rate
    def __init__(self, x, y, fastest_sprite_speed, game_fps):
        Sprite.__init__(self, x, y, fastest_sprite_speed, game_fps)
        self.img = 0          # image bank number from resource file for bird animation
        self.u = 17            # initial bird horizontal position in image in resource file
        self.v = 33           # initial bird vertical position in image in resource file
        self.w = self.SPRITE_WIDTH
        self.h = self.SPRITE_HEIGHT
        self.col = 2          # bird transparent color
        self.frame = random.randint(0,1)
        self.sequence = [0, 1]
        self.animation_size = len(self.sequence)

        # each sprite starts with a randomly-selected velocity (direction)
        self.velocity_x = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
        self.velocity_y = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
        
        # avoid motionless sprites
        while self.velocity_x == 0 and self.velocity_y == 0:
            print('Motionless sprite. Resetting velocity')
            self.velocity_x = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
            self.velocity_y = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
            

    def move(self):
        # Choose next ball in animation sequence. 
        # There are two ball frames
        if self.animate_clock % math.ceil((self.game_fps * self.fastest_sprite_speed)//self.SPRITE_FPS) == 0:
            self.frame = self.frame + 1
        if self.frame > self.animation_size -1:
            self.frame = 0
        self.u = 17 + 8 * self.sequence[self.frame]
        self.animate_clock = self.animate_clock + 1
        print(self.frame, self.sequence[self.frame])

        self.x += self.velocity_x
        self.y -= self.velocity_y

__all__ = ["Ball", "Bird"]
