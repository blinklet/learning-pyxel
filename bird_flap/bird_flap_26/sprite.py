import pyxel
import random
import math
import decimal

class Sprite:
    # Class attributes used in game program to find properties of the class
    SPRITE_WIDTH = 6
    SPRITE_HEIGHT = 6
    SPRITE_SPEED = 0
    SPRITE_FPS = 3            # animation frame rate

    def __init__(self, x, y, fastest_sprite_speed, game_fps):
        self.x = x            # real sprite position on pixelated screen
        self.y = y            # real sprite position on pixelated screen
        self.old_x = x
        self.old_y = y
        self.img = 0          # image bank number from resource file
        self.sequence = ((1, 9), (9, 9), (17, 9))  # x, y coordinates of sprite animation frames
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file
        self.w = self.SPRITE_WIDTH
        self.h = self.SPRITE_HEIGHT
        self.col = 2          # sprite transparent color
        self.animate_clock = 0
        self.animation_size = len(self.sequence) - 1
        self.frame = random.randint(0,self.animation_size)  # start animation at a random frame
        self.fastest_sprite_speed = fastest_sprite_speed
        self.game_fps = game_fps
        
        self.previous_collision_detected = False  # Flag to prevent sprite detecting collision with two or more sprites
        
        # each sprite starts with a randomly-selected velocity (direction)
        self.velocity_x = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
        self.velocity_y = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
        
        # avoid motionless sprites
        if self.SPRITE_SPEED == 0:
            self.velocity_x = 0
            self.velocity_y = 0
        else:
            while self.velocity_x == 0 and self.velocity_y == 0:
                print('Motionless sprite. Resetting velocity')
                self.velocity_x = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
                self.velocity_y = random.randint(-1, 1) * (self.SPRITE_SPEED / fastest_sprite_speed)
                
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

    def find_direction(self):
        if self.velocity_x > 0 and self.velocity_y > 0:
            return("up-right")
        elif self.velocity_x < 0 and self.velocity_y > 0:
            return("up-left")
        elif self.velocity_x > 0 and self.velocity_y < 0:
            return("down-right")
        elif self.velocity_x < 0 and self.velocity_y < 0:
            return("down-left")
        elif self.velocity_x == 0 and self.velocity_y > 0:
            return("up")
        elif self.velocity_x == 0 and self.velocity_y < 0:
            return("down")
        elif self.velocity_x > 0 and self.velocity_y == 0:
            return("right")
        elif self.velocity_x < 0 and self.velocity_y == 0:
            return("left")
        else:
            return("stationary")

    def smooth(self):
        # returns displayable x and y values that do not cause jitter
        direction = self.find_direction()
        if direction in ["up-right","up-left","down-right","down-left"]:
            test_x = abs(int(self.old_x) - int(self.x))
            test_y = abs(int(self.old_y) - int(self.y))
            if test_x != test_y:   # if jitter exists
                if direction == "up-right":
                    self.x = self.x + (self.SPRITE_SPEED/self.fastest_sprite_speed) # change x speed to sync up jitter
                    # print(direction, "real:", self.x, self.y, "disp", math.ceil(self.x), int(self.y))
                    # return math.ceil(self.x), int(self.y)  # round up X, round down Y
                    return self.x, self.y
                elif direction == "up-left":
                    self.x = self.x - (self.SPRITE_SPEED/self.fastest_sprite_speed) # change x speed to sync up jitter
                    # print(direction, "real:", self.x, self.y, "disp", math.ceil(self.x), int(self.y))
                    # return math.ceil(self.x), int(self.y)  # round up X, round down Y
                    return self.x, self.y
                elif direction == "down-right":
                    self.x = self.x + (self.SPRITE_SPEED/self.fastest_sprite_speed) # change x speed to sync up jitter
                    # print(direction, "real:", self.x, self.y, "disp", int(self.x), math.ceil(self.y))
                    # return int(self.x), math.ceil(self.y)  # round down X, round up Y
                    return self.x, self.y
                elif direction =="down-left":
                    self.x = self.x - (self.SPRITE_SPEED/self.fastest_sprite_speed) # change x speed to sync up jitter
                    # print(direction, "real:", self.x, self.y, "disp", int(self.x), math.ceil(self.y))
                    # return int(self.x), math.ceil(self.y)  # round down X, round up Y
                    return self.x, self.y
            else:
                # print(direction, "real:", self.x, self.y, "disp", int(self.x), int(self.y))
                # return int(self.x), int(self.y)  # round everything down
                return self.x, self.y
        else:
            # print(direction, "real:", self.x, self.y, "disp", int(self.x), int(self.y))
            # return int(self.x), int(self.y)  # round everything down
            return self.x, self.y

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
        # Choose next sprite in animation sequence. There are three frames
        # the frame sequence to be: 0, 1, 2, 0, 1, 2,...        
        if self.animate_clock % math.ceil((self.game_fps * self.fastest_sprite_speed)//self.SPRITE_FPS) == 0:
            self.animate_clock = 0 
            self.frame = self.frame + 1
        if self.frame > self.animation_size:
            self.frame = 0
        #print(self.frame)
        self.u = self.sequence[self.frame][0]
        self.v = self.sequence[self.frame][1]
        self.animate_clock = self.animate_clock + 1

    def move(self):
        self.old_x = self.x
        self.old_y = self.y
        self.facing = self.face()
        self.x += self.velocity_x
        self.y -= self.velocity_y
    

    def draw(self):
        self.width = self.w * self.facing 
        xx, yy = self.smooth()
        pyxel.blt(xx, yy, self.img, self.u, self.v, self.width, self.h, self.col)

