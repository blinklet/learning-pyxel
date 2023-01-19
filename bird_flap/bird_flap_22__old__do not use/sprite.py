import pyxel
import random

class Sprite:
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    SPRITE_SPEED = 1
    def __init__(self, x, y, animate_speed):
        self.x = int(x)            # sprite position on pixelated screen
        self.y = int(y)            # sprite position on pixelated screen
        self.real_x = x       # sprite's real position in sub-pixel resolution
        self.real_y = y       # sprite's real position in sub-pixel resolution
        self.old_x = x        # sprite's previous real position on screen (used in de-jitter calculations)
        self.old_y = y        # sprite's previous real position on screen (used in de-jitter calculations)
        self.img = 0          # image bank number from resource file
        self.u = 1            # initial sprite horizontal position in image in resource file
        self.v = 9            # initial sprite vertical position in image in resource file
        self.w = self.SPRITE_WIDTH
        self.h = self.SPRITE_HEIGHT
        self.col = 2          # sprite transparent color
        self.animate_clock = animate_speed # animate_speed is the speed of the fastest sprite in the game

        self.previous_collision_detected = False  # Flag to prevent sprite detecting collision with two or more sprites
        self.start_sprite = random.randint(0,2)  # each sprite starts at a random point in the sprite animation
        
        # each sprite starts with a randomly-selected velocity (direction)
        self.velocity_x = random.randint(-1, 1)  
        self.velocity_y = random.randint(-1, 1)
        
        # avoid motionless sprites
        while self.velocity_x == 0 and self.velocity_y == 0:
            print('Motionless sprite. Resetting velocity')
            self.velocity_x = random.randint(-1, 1)
            self.velocity_y = random.randint(-1, 1) 
            
        # each sprite starts facing left or right, depending on velocity on x axis
        self.facing = self.face()

    # Copied "intersects" algorithm from https://github.com/CaffeinatedTech/Python_Nibbles/blob/master/main.py
    def intersects(self, other):
        if (
            other.x + other.w >= self.x + self.velocity_x
            and self.x + self.w  >= other.x + other.velocity_x
            and other.y + other.h >= self.y - self.velocity_y  # y axis goes from 0 to negative so we subtract velocity_y instead of adding
            and self.y + self.h  >= other.y - other.velocity_y
            ):
            return True
        else:
            return False

    def reached_screen_edge(self,screen_x,screen_y):
        if self.x <= 0 or (self.x + self.w) >= screen_x:
            return True
        elif self.y <= 0 or (self.y + self.h) >= screen_y:
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
        if (self.y + self.h) >= screen_y:  # bottom edge
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
            
    def fix_jitter(self):
        if abs(self.velocity_x > 0) and abs(self.velocity_y > 0):  # if moving diagonally
            if abs(self.old_x - self.real_x) > abs(self.old_y - self.y): 
                x = round(self.x)
                y = round(self.y + (x - self.x) * self.velocity_y / self.velocity_x)
                self.y = y
            elif abs(self.old_x - self.x) <= abs(self.old_y - self.y):
                y = round(self.y)
                x = round(self.x + (y - self.y) * self.velocity_x / self.velocity_y)
                self.x = x

    def move(self):
        # This is a very basic move function
        # Each sprite will have it's own move method which will
        # be defined in the sprite's subclass
        self.old_x = self.x
        self.old_y = self.real_y
        self.real_x += self.velocity_x
        self.real_y += self.velocity_y
        self.x += self.velocity_x
        self.y -= self.velocity_y

    # def fix_jitter(self):
    #     if abs(self.velocity_x > 0) or abs(self.velocity_y > 0):
    #         if abs(self.old_x - self.x) > abs(self.old_y - self.y): 
    #             x = round(self.x)
    #             y = round(self.y + (x - self.x) * self.velocity_y / self.velocity_x)
    #             self.y = y
    #         elif abs(self.old_x - self.x) <= abs(self.old_y - self.y):
    #             y = round(self.y)
    #             x = round(self.x + (y - self.y) * self.velocity_x / self.velocity_y)
    #             self.x = x

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w * self.facing, self.h, self.col)

