import pyxel
import random

SCREEN_SIZE_X = 60
SCREEN_SIZE_Y = 60
OUTSIDE_SCREEN_SPACE_X = 0
OUTSIDE_SCREEN_SPACE_Y = 0
BIRD_WIDTH = 8
BIRD_HEIGHT = 8
FPS = 12
BACKGROUND_COLOR = 2


class Bird:
    def __init__(self, x, y):
        self.x = x            # bird position on screen
        self.y = y            # bird position on screen
        self.img = 0          # image bank number from resource file
        self.u = 0            # initial sprite position in image in resource file
        self.v = 16           # initial sprite position in image in resource file
        self.w = BIRD_WIDTH   # sprite width
        self.h = BIRD_HEIGHT  # sprite height
        self.col = 2          # sprite transparent color

        self.is_same_bird = False  # Flag to prevent bird detecting collision with itself
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
            other.x + other.w >= self.x
            and self.x + self.w >= other.x
            and other.y + other.h >= self.y
            and self.y + self.h >= other.y
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
        if self.x <= 0:   # left edge
            self.velocity_x = 1
        if self.x >= screen_x:  # right edge
            self.velocity_x = -1
        if self.y <= 0:  # top edge
            self.velocity_y = -1
        if self.y >= screen_y:  # bottom edge
            self.velocity_y = 1   

    def face(self):
        if self.velocity_x != 0:
            return self.velocity_x
        else:
            return self.velocity_y

    def move(self):
        # Choose next sprite in animation sequence (there are three frames)
        self.u = 8 * ((pyxel.frame_count + self.start_sprite) % 3)

        # set direction bird will face when moving
        self.facing = self.face()

        # move bird
        self.x += self.velocity_x
        self.y -= self.velocity_y

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w * self.facing, self.h, self.col)


class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE_X, SCREEN_SIZE_Y, fps=FPS)
        pyxel.load("../assets/platformer.pyxres")
        self.screen_x = pyxel.width + (2 *OUTSIDE_SCREEN_SPACE_X) - BIRD_WIDTH
        self.screen_y = pyxel.height + (2 * OUTSIDE_SCREEN_SPACE_Y) - BIRD_HEIGHT
        self.bird_list = []
        self.max_birds = ((pyxel.width // BIRD_WIDTH) * (pyxel.height // BIRD_HEIGHT))
        
        # camera(8,8) creates an 8-pixel wide space on the top and left side of the 
        # screen that we can address without using negative numbers
        pyxel.camera(OUTSIDE_SCREEN_SPACE_X, OUTSIDE_SCREEN_SPACE_Y)
        
        pyxel.run(self.update, self.draw)

    def add_new_bird(self):
        # Create new bird in random position
        new_bird_x = random.randint(1, pyxel.width - BIRD_WIDTH - 1)
        new_bird_y = random.randint(1, pyxel.height - BIRD_HEIGHT - 1)
        new_bird = Bird(new_bird_x, new_bird_y)

        # Check if new bird object overlaps or collides with any existing bird
        counter = 0
        if len(self.bird_list) > 0:
            try_again = True
            while counter < 10 and try_again:
                try_again = False
                for bird in self.bird_list:
                    if bird.intersects(new_bird):
                        try_again = True
                        new_bird_x = random.randint(1, pyxel.width - BIRD_WIDTH - 1)
                        new_bird_y = random.randint(1, pyxel.height - BIRD_HEIGHT - 1)
                        new_bird = Bird(new_bird_x, new_bird_y)
                        break
                if try_again == True:
                    print(f'{counter} - No space') 
                    counter += 1

        if counter <10:
            self.bird_list.append(Bird(new_bird_x, new_bird_y)) 

    def remove_bird(self):
        if len(self.bird_list) > 0:
            self.bird_list.pop(0)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE) and len(self.bird_list) < self.max_birds:
            self.add_new_bird()

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.remove_bird()

        # detect collisions and move birds
        bird_count = len(self.bird_list)
        b = 0
        while b < bird_count:
            # select bird from the bird list
            bird = self.bird_list[b]
            # make temporary list that contains all other birds
            other_birds_list = [other_bird for other_bird in self.bird_list if other_bird != bird]

            if bird.reached_screen_edge(self.screen_x,self.screen_y):
                bird.bounce_off_edge(self.screen_x,self.screen_y)

            # Check if any other bird has collided with the bird
            for other_bird in other_birds_list:
                if bird.intersects(other_bird): 
                    bird.velocity_x, other_bird.velocity_x = other_bird.velocity_x, bird.velocity_x
                    bird.velocity_y, other_bird.velocity_y = other_bird.velocity_y, bird.velocity_y

            self.bird_list[b] = bird
            b += 1

        for bird in self.bird_list:
            bird.move()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        for bird in self.bird_list:
            bird.draw()

        
App()