import pyxel
import random
import itertools

SCREEN_SIZE_X = 60
SCREEN_SIZE_Y = 60
OUTSIDE_SCREEN_SPACE_X = 0
OUTSIDE_SCREEN_SPACE_Y = 0
BIRD_WIDTH = 8
BIRD_HEIGHT = 8
BIRD_IMAGE_X = 0
BIRD_IMAGE_Y = 16
BALL_HEIGHT = 6
BALL_WIDTH = 6
MAX_SPRITES_FACTOR = 0.45
FPS = 12
BACKGROUND_COLOR = 2


class Sprite:
    def __init__(self, x, y, w, h, u, v):
        self.x = x            # bird position on screen
        self.y = y            # bird position on screen
        self.img = 0          # image bank number from resource file
        self.u = u            # initial sprite horizontal position in image in resource file
        self.v = v            # initial sprite vertical position in image in resource file
        self.w = w            # sprite width
        self.h = h            # sprite height
        self.col = 2          # sprite transparent color

        self.previous_collision_detected = False  # Flag to prevent bird detecting collision with two or more birds
        self.start_sprite = random.randint(0,2)  # each bird starts at a random point in the sprite animation
        
        self.velocity_x = random.randint(-1, 1)  # each bird starts with a randomly-selected velocity (direction)
        self.velocity_y = random.randint(-1, 1)
        
        while self.velocity_x == 0 and self.velocity_y == 0:  # avoid motionless birds
            print('Motionless bird. Resetting velocity')
            self.velocity_x = random.randint(-1, 1)  # each bird starts with a randomly-selected velocity (direction)
            self.velocity_y = random.randint(-1, 1) 
            
        self.facing = self.face()    # each bird starts facing left or right, depending on velocity on x axis

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
            self.velocity_x = 1
        if self.x + self.velocity_x >= screen_x:  # right edge
            self.velocity_x = -1
        if self.y - self.velocity_y <= 0:  # top edge
            self.velocity_y = -1
        if self.y - self.velocity_y >= screen_y:  # bottom edge
            self.velocity_y = 1   

    def face(self):
        if self.velocity_x != 0:
            return self.velocity_x
        else:
            return self.velocity_y

    def move(self):
        # Choose next sprite in animation sequence. There are three frames
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

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w * self.facing, self.h, self.col)

class Bird(Sprite):
    pass


class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE_X, SCREEN_SIZE_Y, fps=FPS)
        pyxel.load("../assets/platformer.pyxres")
        self.screen_x = pyxel.width + (2 *OUTSIDE_SCREEN_SPACE_X) - BIRD_WIDTH
        self.screen_y = pyxel.height + (2 * OUTSIDE_SCREEN_SPACE_Y) - BIRD_HEIGHT
        self.bird_list = []
        self.max_birds = ((pyxel.width // BIRD_WIDTH) * (pyxel.height // BIRD_HEIGHT)) * MAX_SPRITES_FACTOR
        
        # camera(8,8) creates an 8-pixel wide space on the top and left side of the 
        # screen that we can address without using negative numbers
        pyxel.camera(OUTSIDE_SCREEN_SPACE_X, OUTSIDE_SCREEN_SPACE_Y)
        
        pyxel.run(self.update, self.draw)

    def generate_bird(self):
        # Create new bird in random position
        new_bird_x = random.randint(1, pyxel.width - BIRD_WIDTH - 1)
        new_bird_y = random.randint(1, pyxel.height - BIRD_HEIGHT - 1)
        return(Bird(new_bird_x, new_bird_y, BIRD_WIDTH, BIRD_HEIGHT, BIRD_IMAGE_X, BIRD_IMAGE_Y))

    def add_new_bird(self):
        # Create new bird in random position
        new_bird = self.generate_bird()

        # Check if new bird object overlaps or collides with any existing bird
        counter = 0
        if len(self.bird_list) > 0:
            try_again = True
            while counter < 10 and try_again:
                try_again = False
                for bird in self.bird_list:
                    if bird.intersects(new_bird):
                        try_again = True
                        new_bird = self.generate_bird()   # new bird in new random location
                        break   # no need to continue after first collision found
                if try_again == True:
                    print(f'{counter} - No space') 
                    counter += 1
        
        # if the loop ran ten times without finding free space for a new bird, do nothing
        if counter < 10:
            self.bird_list.append(new_bird)

    def remove_bird(self):
        if len(self.bird_list) > 0:
            self.bird_list.pop(0)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE):
            if len(self.bird_list) < self.max_birds:
                self.add_new_bird()
            else:
                print("Maximum sprites reached")

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.remove_bird()

        # detect collisions and move birds.
        # itertools offers a way to do this. 
        # See https://stackoverflow.com/questions/16603282/how-to-compare-each-item-in-a-list-with-the-rest-only-once
        # for examples of various ways to compare items in a list (without multiple comparisons)
        # https://docs.python.org/3/library/itertools.html#itertools.combinations
        #
        # maybe try different approach: https://gamedev.net/forums/topic/701045-axis-aligned-rectangle-collision-handling/5400917/

        # Check screen collision first (new velocity in bounce_off_edge function)
        for bird in self.bird_list:
            if bird.reached_screen_edge(self.screen_x,self.screen_y):
                bird.previous_collision_detected = True  # do not change direction after this collision, during this round
                bird.bounce_off_edge(self.screen_x,self.screen_y)

        for bird, other_bird in itertools.combinations(self.bird_list, 2):
            if other_bird.previous_collision_detected == False: 
                if bird.intersects(other_bird): 
                    other_bird.previous_collision_detected = True  # set collision flag on other birds where detected with current bird
                    bird.velocity_x, other_bird.velocity_x = other_bird.velocity_x, bird.velocity_x
                    bird.velocity_y, other_bird.velocity_y = other_bird.velocity_y, bird.velocity_y
        
        for bird in self.bird_list:
            bird.previous_collision_detected = False  # reset collisions on all birds
            bird.move()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        for bird in self.bird_list:
            bird.draw()

        
App()