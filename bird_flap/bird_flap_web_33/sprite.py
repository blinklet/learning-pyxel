import pyxel
import random

class Sprite:
    # Class attributes used in game program to find properties of the class
    TYPE = "sprite"
    SPRITE_WIDTH = 6
    SPRITE_HEIGHT = 6
    SPRITE_SPEED = 0
    SPRITE_FPS = 3  # animation frame rate

    def __init__(self, fastest_sprite_speed, game_fps):
        self.r = self.SPRITE_WIDTH // 2
        self.x = pyxel.rndf(self.r + 1, pyxel.width - self.r - 1)            
        self.y = pyxel.rndf(self.r + 1, pyxel.height - self.r - 17) # minus 17 to leave space for walker
        self.img = 0          # image bank number from resource file
        self.sequence = ((1, 9), (9, 9), (17, 9))  # x, y coordinates of sprite animation frames
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file
        self.w = self.SPRITE_WIDTH
        self.h = self.SPRITE_HEIGHT
        self.col = 2          # sprite transparent color
        self.animate_clock = 0
        self.animation_size = len(self.sequence) - 1
        self.frame = pyxel.rndi(0,self.animation_size)  # start animation at a random frame
        self.fastest_sprite_speed = fastest_sprite_speed
        self.game_fps = game_fps
        
        self.previous_collision_detected = False  # Flag to prevent sprite detecting collision with two or more sprites
        
        self.speed_ratio = self.SPRITE_SPEED / fastest_sprite_speed

        # each sprite starts with a randomly-selected velocity (direction)
        self.velocity_x = pyxel.rndi(-1, 1) * self.speed_ratio
        self.velocity_y = -2 * self.speed_ratio  # always move either down at start
        
        # avoid motionless sprites
        if self.SPRITE_SPEED == 0:
            self.velocity_x = 0
            self.velocity_y = 0
        else:
            while self.velocity_x == 0 and self.velocity_y == 0:
                print('Motionless sprite. Resetting velocity')
                self.velocity_x = pyxel.rndi(-1, 1) * self.speed_ratio
                self.velocity_y = -2
                
        # each sprite starts facing left or right, depending on velocity on x axis
        self.facing = self.face()

    # Copied from App.update function in pyxel_examples/06_click_game.py
    def intersects(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        total_r = (self.r) + (other.r)
        if (dx * dx) + (dy * dy) < (total_r * total_r):
            return True
        else:
            return False

    def reached_screen_edge(self,screen_x,screen_y):
        if self.x <= 0 or (self.x + self.w) >= screen_x:
            return True
        elif self.y <= 0 or (self.y + self.h) >= screen_y - 3:
            return True
        else:
            return False

    def bounce_off_edge(self,screen_x,screen_y):
        if self.x <= 0:   # left edge
            self.velocity_x = abs(self.velocity_x)
        if (self.x + self.w) >= screen_x:  # right edge
            self.velocity_x = -abs(self.velocity_x)
        if self.y <= 0:  # top edge
            self.velocity_y = -abs(self.velocity_y)
        if (self.y + self.h) >= screen_y - 3:  # bottom edge
            self.velocity_y = abs(self.velocity_y) 

    def face(self):
        if self.velocity_x == 0:
            if self.velocity_y >= 0:
                return 1
            else:
                return -1
        if self.velocity_x > 0:
            return 1
        if self.velocity_x < 0:
            return -1

    def animate(self):
        # Animation speed is relative to game_fps and
        # animation will cycle x times per y frames where:
        #      x = length of animation
        #      y = FPS value     
        step = int((self.game_fps * self.fastest_sprite_speed)//self.SPRITE_FPS)
        if step == 0:
            step = 1
        if self.animate_clock % step == 0:
            self.animate_clock = 0 
            self.frame = self.frame + 1
        if self.frame > self.animation_size:
            self.frame = 0

        self.u = self.sequence[self.frame][0]
        self.v = self.sequence[self.frame][1]
        self.animate_clock = self.animate_clock + 1

    def update(self):
        self.facing = self.face()
        self.x += self.velocity_x
        self.y -= self.velocity_y
        if self.reached_screen_edge(pyxel.width,pyxel.height):
            self.bounce_off_edge(pyxel.width,pyxel.height)
    
    def draw(self):
        self.width = self.w * self.facing 
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.width, self.h, self.col)
