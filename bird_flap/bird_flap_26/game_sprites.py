from sprite import Sprite
import pyxel
import math


class Bird(Sprite):
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    SPRITE_SPEED = 1
    SPRITE_FPS = 3            # animation frame rate
    def __init__(self, x, y, fastest_sprite_speed, game_fps):
        Sprite.__init__(self, x, y, fastest_sprite_speed, game_fps)
        self.sequence = ((0, 16),(8, 16), (16, 16), (8, 16))  # x-coordinates of sprite animation frames
        self.animation_size = len(self.sequence) - 1
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file

class Ball(Sprite):
    SPRITE_WIDTH = 6
    SPRITE_HEIGHT = 6
    SPRITE_SPEED = 5
    SPRITE_FPS = 2            # animation frame rate
    def __init__(self, x, y, fastest_sprite_speed, game_fps):
        Sprite.__init__(self, x, y, fastest_sprite_speed, game_fps)
        self.sequence = ((17, 33), (25, 33))  # x-coordinates of sprite animation frames
        self.animation_size = len(self.sequence) - 1
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file

class Walker1(Sprite):
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    SPRITE_SPEED = 2
    SPRITE_FPS = 4           # animation frame rate
    def __init__(self, x, y, fastest_sprite_speed, game_fps):
        Sprite.__init__(self, x, y, fastest_sprite_speed, game_fps)
        self.sequence = ((0, 24), (8, 24))  # x-coordinates of sprite animation frames
        self.animation_size = len(self.sequence) - 1
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file

    def smooth(self):
        return self.x, self.y

    def move(self, direction):
        # add custom moves for left and right
        self.old_x = self.x
        self.old_y = self.y
        if direction == "left":
            if self.x > 0:
                self.facing = -1
                self.x -= self.SPRITE_SPEED
        if direction == "right":
            if self.x < pyxel.width - self.SPRITE_WIDTH:
                self.x += self.SPRITE_SPEED
                self.facing = 1

    def animate(self):
        # Add custom animation. I want animation happen when I press the keys  
        if self.animate_clock % math.ceil(self.game_fps/self.SPRITE_FPS) == 0:
            self.animate_clock = 0 
            self.frame = self.frame + 1
        if self.frame > self.animation_size:
            self.frame = 0
        #print(self.frame)
        self.u = self.sequence[self.frame][0]
        self.v = self.sequence[self.frame][1]
        self.animate_clock = self.animate_clock + 1

    #   16 24   24 24

