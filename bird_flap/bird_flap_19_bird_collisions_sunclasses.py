import pyxel
import random
import itertools

SCREEN_SIZE_X = 60
SCREEN_SIZE_Y = 60
OUTSIDE_SCREEN_SPACE_X = 0
OUTSIDE_SCREEN_SPACE_Y = 0
MAX_SPRITES_FACTOR = 0.45
FPS = 12
BACKGROUND_COLOR = 2


class Sprite:
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    def __init__(self, x, y):
        self.x = x            # sprite position on screen
        self.y = y            # sprite position on screen
        self.img = 0          # image bank number from resource file
        self.u = 1            # initial sprite horizontal position in image in resource file
        self.v = 9            # initial sprite vertical position in image in resource file
        self.w = self.SPRITE_WIDTH
        self.h = self.SPRITE_HEIGHT
        self.col = 2          # sprite transparent color

        self.previous_collision_detected = False  # Flag to prevent sprite detecting collision with two or more sprites
        self.start_sprite = random.randint(0,2)  # each sprite starts at a random point in the sprite animation
        
        self.velocity_x = random.randint(-1, 1)  # each sprite starts with a randomly-selected velocity (direction)
        self.velocity_y = random.randint(-1, 1)
        
        while self.velocity_x == 0 and self.velocity_y == 0:  # avoid motionless sprites
            print('Motionless sprite. Resetting velocity')
            self.velocity_x = random.randint(-1, 1)  # each sprite starts with a randomly-selected velocity (direction)
            self.velocity_y = random.randint(-1, 1) 
            
        self.facing = self.face()    # each sprite starts facing left or right, depending on velocity on x axis

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
        if self.x <= 0 or self.x >= screen_x:
            return True
        elif self.y <= 0 or self.y >= screen_y:
            return True
        else:
            return False

    def bounce_off_edge(self,screen_x,screen_y):
        if self.x + self.velocity_x <= 0:   # left edge
            self.velocity_x = abs(self.velocity_x)
        if self.x + self.velocity_x >= screen_x:  # right edge
            self.velocity_x = -abs(self.velocity_x)
        if self.y - self.velocity_y <= 0:  # top edge
            self.velocity_y = -abs(self.velocity_y)
        if self.y - self.velocity_y >= screen_y:  # bottom edge
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
        
    def move(self):
        # Each sprite will have it's own move method which will
        # be defined in the sprite's subclass
        self.x += self.velocity_x
        self.y -= self.velocity_y

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w * self.facing, self.h, self.col)

class Bird(Sprite):
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    def __init__(self, x, y):
        Sprite.__init__(self, x, y)
        self.img = 0          # image bank number from resource file for bird animation
        self.u = 0            # initial bird horizontal position in image in resource file
        self.v = 16           # initial bird vertical position in image in resource file
        self.w = self.SPRITE_WIDTH            # bird width
        self.h = self.SPRITE_HEIGHT            # bird height
        self.col = 2          # bird transparent color
        self.start_sprite = random.randint(0,2)

    def move(self):
        # Choose next Bird in animation sequence. There are three bird frames
        # but we want to cycle back and forth across the frames so we want
        # the frame sequence to be: 0, 1, 2, 1, 0, 1, 2, 1, 0,...
        frame = (pyxel.frame_count + self.start_sprite) % 4
        if frame == 3:
            frame = 1
        self.u = 8 * frame
       
        # set direction bird will face when moving
        self.facing = self.face()

        # move bird
        self.x += self.velocity_x
        self.y -= self.velocity_y


class Ball(Sprite):
    SPRITE_WIDTH = 6
    SPRITE_HEIGHT = 6
    def __init__(self, x, y):
        Sprite.__init__(self, x, y)
        self.img = 0          # image bank number from resource file for bird animation
        self.u = 17            # initial bird horizontal position in image in resource file
        self.v = 33           # initial bird vertical position in image in resource file
        self.w = self.SPRITE_WIDTH
        self.h = self.SPRITE_HEIGHT
        self.col = 2          # bird transparent color
        self.start_sprite = random.randint(0,1)
        self.velocity_x = 2  # each sprite starts with a randomly-selected velocity (direction)
        self.velocity_y = 2

    def move(self):
        # Choose next ball in animation sequence. 
        # There are two ball frames
        frame = (pyxel.frame_count + self.start_sprite) % 2
        self.u = 17 + (8 * frame)

        # move ball
        self.x += self.velocity_x
        self.y -= self.velocity_y


class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE_X, SCREEN_SIZE_Y, fps=FPS)
        pyxel.load("../assets/platformer.pyxres")
        self.screen_x = pyxel.width + (2 *OUTSIDE_SCREEN_SPACE_X) - Sprite.SPRITE_WIDTH
        self.screen_y = pyxel.height + (2 * OUTSIDE_SCREEN_SPACE_Y) - Sprite.SPRITE_HEIGHT
        self.sprite_list = []
        self.max_sprites = ((pyxel.width // Sprite.SPRITE_WIDTH) * (pyxel.height // Sprite.SPRITE_HEIGHT)) * MAX_SPRITES_FACTOR
        
        # camera(x,y) creates an x-pixel wide and y-pixel high space on the top and left side of the 
        # screen that we can address without using negative numbers
        pyxel.camera(OUTSIDE_SCREEN_SPACE_X, OUTSIDE_SCREEN_SPACE_Y)
        
        pyxel.run(self.update, self.draw)

    def generate_sprite(self, sprite_type):
        # Create new sprite in random position
        if sprite_type == "bird":
            new_bird_x = random.randint(1, pyxel.width - Bird.SPRITE_WIDTH - 1)
            new_bird_y = random.randint(1, pyxel.height - Bird.SPRITE_HEIGHT - 1)
            sprite = Bird(new_bird_x, new_bird_y)
        if sprite_type == "ball":
            new_ball_x = random.randint(1, pyxel.width - Ball.SPRITE_WIDTH - 1)
            new_ball_y = random.randint(1, pyxel.height - Ball.SPRITE_HEIGHT - 1)
            sprite = Ball(new_ball_x, new_ball_y)
        return(sprite)

    def add_new_sprite(self, sprite_type):
        # Create new sprite in random position
        new_sprite = self.generate_sprite(sprite_type)

        # Check if new sprite object overlaps or collides with any existing sprite
        counter = 0
        if len(self.sprite_list) > 0:
            try_again = True
            while counter < 10 and try_again:
                try_again = False
                for sprite in self.sprite_list:
                    if sprite.intersects(new_sprite):
                        try_again = True
                        new_sprite = self.generate_sprite(sprite_type)   # new sprite in new random location
                        break   # no need to continue after first collision found
                if try_again == True:
                    print(f'{counter} - No space') 
                    counter += 1
        
        # if the loop ran ten times without finding free space for a new sprite, do nothing
        if counter < 10:
            self.sprite_list.append(new_sprite)

    def remove_sprite(self):
        if len(self.sprite_list) > 0:
            self.sprite_list.pop(0)

    def at_max_sprites(self):
        if len(self.sprite_list) >= self.max_sprites:
            print("Maximum sprites reached")
            return True
        else:
            return False

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_B):
            if not self.at_max_sprites():
                self.add_new_sprite("bird")

        if pyxel.btnp(pyxel.KEY_V):
            if not self.at_max_sprites():
                self.add_new_sprite("ball")            

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.remove_sprite()

        # detect collisions and move birds.
        # itertools offers a way to do this. 
        # See https://stackoverflow.com/questions/16603282/how-to-compare-each-item-in-a-list-with-the-rest-only-once
        # for examples of various ways to compare items in a list (without multiple comparisons)
        # https://docs.python.org/3/library/itertools.html#itertools.combinations
        #
        # maybe try different approach: https://gamedev.net/forums/topic/701045-axis-aligned-rectangle-collision-handling/5400917/

        # Check screen collision first (new velocity in bounce_off_edge function)
        for sprite in self.sprite_list:
            if sprite.reached_screen_edge(self.screen_x,self.screen_y):
                sprite.previous_collision_detected = True  # do not change direction after this collision, during this round
                sprite.bounce_off_edge(self.screen_x,self.screen_y)

        for sprite, other_sprite in itertools.combinations(self.sprite_list, 2):
            if other_sprite.previous_collision_detected == False: 
                if sprite.intersects(other_sprite): 
                    other_sprite.previous_collision_detected = True  # set collision flag on other birds where detected with current sprite
                    sprite.velocity_x, other_sprite.velocity_x = other_sprite.velocity_x, sprite.velocity_x
                    sprite.velocity_y, other_sprite.velocity_y = other_sprite.velocity_y, sprite.velocity_y
        
        for sprite in self.sprite_list:
            sprite.previous_collision_detected = False  # reset collisions on all birds
            sprite.move()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        for sprite in self.sprite_list:
            sprite.draw()

        
App()