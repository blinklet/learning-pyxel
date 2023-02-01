from sprite import Sprite
import pyxel

class Bird(Sprite):
    TYPE = "bird"
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    SPRITE_SPEED = 1
    SPRITE_FPS = 3            # animation frame rate
    def __init__(self, fastest_sprite_speed, game_fps):
        Sprite.__init__(self, fastest_sprite_speed, game_fps)
        self.r = self.SPRITE_WIDTH / 2
        self.x = pyxel.rndf(1, pyxel.width - self.SPRITE_WIDTH - 1)
        self.y = -8 # leave space for walker
        self.sequence = ((0, 16),(8, 16), (16, 16), (8, 16))  # x-coordinates of sprite animation frames
        self.animation_size = len(self.sequence) - 1
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file

class Ball(Sprite):
    TYPE = "ball"
    SPRITE_WIDTH = 6
    SPRITE_HEIGHT = 6
    SPRITE_SPEED = 2
    SPRITE_FPS = 2            # animation frame rate
    def __init__(self, fastest_sprite_speed, game_fps):
        Sprite.__init__(self, fastest_sprite_speed, game_fps)
        self.r = self.SPRITE_WIDTH / 2
        self.x = pyxel.rndf(1, pyxel.width - self.SPRITE_WIDTH - 1)
        self.y = -8
        self.sequence = ((17, 33), (25, 33))  # x-coordinates of sprite animation frames
        self.animation_size = len(self.sequence) - 1
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file

class Walker1(Sprite):
    TYPE = "walker"
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    SPRITE_SPEED = 3         # do not use this constant. Use the walker_speed variable, instead
                             # SPRITE_SPEED still used to find max_sprite_speed and set speed_ratio
                             # so it still determines the "relative" speed of the walker
                             # compared to other sprites
    SPRITE_FPS = 3           # animation frame rate
    def __init__(self, fastest_sprite_speed, game_fps, hit):
        Sprite.__init__(self, fastest_sprite_speed, game_fps)
        self.r = self.SPRITE_WIDTH / 2
        self.x = pyxel.rndf(1, pyxel.width - self.SPRITE_WIDTH - 1)
        self.y = pyxel.height - self.SPRITE_HEIGHT - 3
        self.sequence = ((0, 24), (8, 24))  # x-coordinates of sprite animation frames
        self.animation_size = len(self.sequence) - 1
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file
        self.walker_speed = 1 # pixels moved per clock. Set to 1 or lower
        self.hit = hit
        self.hit_clock = 0


    def smooth(self):
        return self.x, self.y

    def animate(self):
        # Add response to a hit
        step = int((self.game_fps * self.fastest_sprite_speed)//self.SPRITE_FPS)
        if step == 0:
            step = 1
        if self.animate_clock % step == 0:
            self.animate_clock = 0 
            self.frame = self.frame + 1
        if self.frame > self.animation_size:
            self.frame = 0
        # print(self.frame)
        if self.hit:
            self.u = self.sequence[self.frame][0] + 16 # the red sprites are 16 to the right
            self.hit_clock = self.hit_clock + 1
            if self.hit_clock % step == 0:
                self.hit = False
                self.hit_clock = 0
        else:
            self.u = self.sequence[self.frame][0]
        self.v = self.sequence[self.frame][1]
        self.animate_clock = self.animate_clock + 1

    def update(self):
        # add custom moves for left and right 
        if pyxel.btnp(pyxel.KEY_A, 1, 1) or pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
            if self.x > 0:
                self.facing = -1
                self.x -= self.walker_speed
        if pyxel.btnp(pyxel.KEY_F, 1, 1) or pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
            if self.x < pyxel.width - self.SPRITE_WIDTH:
                self.x += self.walker_speed
                self.facing = 1

