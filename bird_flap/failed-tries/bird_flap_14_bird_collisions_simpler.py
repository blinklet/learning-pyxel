import pyxel
import random
import copy

SCREEN_SIZE_X = 30
SCREEN_SIZE_Y = 30
OUTSIDE_SCREEN_SPACE_X = 0
OUTSIDE_SCREEN_SPACE_Y = 0
BIRD_WIDTH = 8
BIRD_HEIGHT = 8
FPS = 4
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
        if self.velocity_x == 0:
            self.velocity_y = random.choice([-1, 1]) # avoid motionless birds
        else:
            self.velocity_y = random.randint(-1, 1)

        self.facing = 1    # each bird starts facing left or right, depending on velocity on x axis

    def intersects(self, other_x, other_y, other_w, other_h):
        is_intersected = False
        if (
            other_x + other_w >= self.x
            and self.x + self.w >= other_x
            and other_y + other_h >= self.y
            and self.y + self.h >= other_y
        ):
            is_intersected = True
        return is_intersected

    # Copied intersects function from https://github.com/CaffeinatedTech/Python_Nibbles/blob/master/main.py
    def collides(self, other_x, other_y, other_w, other_h):
        # check corners
        if (
            other_x + other_w == self.x
            and other_y + other_h == self.y
        ):
            return "top_left"

        if (
            self.x + self.w == other_x
            and other_y + other_h == self.y
        ):
            return "top_right"

        if (
            other_x + other_w == self.x
            and self.y + self.h == other_y
        ):
            return "bottom_left"

        if (
            self.x + self.w == other_x
            and self.y + self.h == other_y
        ):
            return "bottom_right"

        # check sides
        if (
            other_x + other_w >= self.x + 1
            and self.x + self.w >= other_x
            and other_y + other_h == self.y
        ):
            return "top"

        if (
            other_x + other_w >= self.x
            and self.x + self.w >= other_x
            and self.y + self.h == other_y
        ):
            return "bottom"

        if (
            other_x + other_w == self.x
            and other_y + other_h >= self.y
            and self.y + self.h >= other_y
        ):
            return "left"

        if (
            self.x + self.w == other_x
            and other_y + other_h >= self.y
            and self.y + self.h >= other_y
        ):
            return "right"
        
        return "none"


    def reached_screen_edge(self,screen_x,screen_y):
        screen_edge_detected = False
        if self.x == 0 or self.x == screen_x:
            # self.velocity_x *= -1
            screen_edge_detected = True

        if self.y == 0 or self.y == screen_y:
            # self.velocity_y *= -1
            screen_edge_detected = True

        return screen_edge_detected

    def bounce_off_edge(self,screen_x,screen_y):
        if self.x == 0 and self.y >= 0 and self.y <= screen_y:
            self.velocity_x = 1
        if self.x == screen_x and self.y >= 0 and self.y <= screen_y:
            self.velocity_x = -1
        if self.y == 0 and self.x >= 0 and self.x <= screen_x:
            self.velocity_y = -1
        if self.y == screen_y and self.x >= 0 and self.x <= screen_x:        
            self.velocity_y = 1   


    def move(self):
        # Choose next sprite in animation sequence (there are three frames)
        self.u = 8 * ((pyxel.frame_count + self.start_sprite) % 3)

        # bird faces right when moving right and left when moving left
        # but if it is only moving up or down, it faces right when going up 
        # and left when going down
        if self.velocity_x != 0:
            self.facing = self.velocity_x
        else:
            self.facing = self.velocity_y

        # move bird
        self.x += self.velocity_x
        self.y -= self.velocity_y

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w * self.facing, self.h, self.col)


class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE_X, SCREEN_SIZE_Y, fps=FPS)
        pyxel.load("../../assets/platformer.pyxres")
        self.screen_x = pyxel.width + OUTSIDE_SCREEN_SPACE_X - BIRD_WIDTH
        self.screen_y = pyxel.height + OUTSIDE_SCREEN_SPACE_Y - BIRD_HEIGHT
        self.bird_list = []
        self.max_birds = ((pyxel.width // BIRD_WIDTH) * (pyxel.height // BIRD_HEIGHT))
        
        # camera(8,8) creates an 8-pixel wide space on the top and left side of the 
        # screen that we can address without using negative numbers
        pyxel.camera(OUTSIDE_SCREEN_SPACE_X, OUTSIDE_SCREEN_SPACE_Y)
        
        pyxel.run(self.update, self.draw)

    def add_new_bird(self):
        new_bird_x = random.randint(1, pyxel.width - BIRD_WIDTH - 1)
        new_bird_y = random.randint(1, pyxel.height - BIRD_HEIGHT - 1)

        counter = 0
        if len(self.bird_list) > 0:
            try_again = True
            while counter < 10 and try_again:
                try_again = False
                for bird in self.bird_list:
                    if bird.intersects(new_bird_x,new_bird_y,BIRD_WIDTH,BIRD_HEIGHT):
                        try_again = True
                        new_bird_x = random.randint(1, pyxel.width - BIRD_WIDTH - 1)
                        new_bird_y = random.randint(1, pyxel.height - BIRD_HEIGHT - 1)
                        break
                if try_again == True:
                    print(f'{counter} - No space') 
                    counter += 1

        if counter <10:
            self.bird_list.append(Bird(new_bird_x, new_bird_y)) 

    def remove_bird(self):
        if len(self.bird_list) > 0:
            self.bird_list.pop()

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE) and len(self.bird_list) < self.max_birds:
            self.add_new_bird()

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.remove_bird()

        if len(self.bird_list) == 1:
            if self.bird_list[0].reached_screen_edge(self.screen_x,self.screen_y):
                self.bird_list[0].bounce_off_edge(self.screen_x,self.screen_y)
            self.bird_list[0].move()
        else:
            bird_count = len(self.bird_list)
            b = 0
            while b < bird_count:
                # make temporary list that contains all other birds except the indexed bird
                bird = self.bird_list[b]
                other_birds = self.bird_list[:b] + self.bird_list[b + 1:]

                # Check if any other bird has collided with the bird
                # Change direction of the bird if it collided 
                for other_bird in other_birds:
                    side = bird.collides(other_bird.x,other_bird.y,other_bird.w,other_bird.h)
                    if side != "none":
                        print(side)
                        if side == "top":
                            if bird.velocity_y == 1:
                                bird.velocity_y = 0
                                if other_bird.velocity_y == 0:
                                    other_bird.velocity = -1
                                if other_bird.velocity_y == 0:
                                    other_bird.velocity_y = 1
                            if bird.velocity_y == 0:
                                bird.velocity_y = -1
                                if other_bird.velocity_y == 1:
                                    other_bird.velocity = 0
                                if other_bird.velocity_y == 0:
                                    other_bird.velocity_y = -1
                            #bird.velocity_y, other_bird.velocity_y = other_bird.velocity_y, bird.velocity_y
                        if side == "bottom":
                            if bird.velocity_y == -1:
                                bird.velocity_y = 0
                            if bird.velocity_y == 0:
                                bird.velocity_y = 1
                            #bird.velocity_y, other_bird.velocity_y = other_bird.velocity_y, bird.velocity_y
                        if side == "left":
                            if bird.velocity_x == -1:
                                bird.velocity_x = 0
                            if bird.velocity_x == 0:
                                bird.velocity_x = 1
                            #bird.velocity_x, other_bird.velocity_x = other_bird.velocity_x, bird.velocity_x
                        if side == "right":
                            if bird.velocity_x == 1:
                                bird.velocity_x = 0
                            if bird.velocity_x == 0:
                                bird.velocity_x = -1
                            #bird.velocity_x, other_bird.velocity_x = other_bird.velocity_x, bird.velocity_x
                        if side == "top_left":
                            bird.velocity_x, other_bird.velocity_x = other_bird.velocity_x, bird.velocity_x
                            bird.velocity_y, other_bird.velocity_y = other_bird.velocity_y, bird.velocity_y
                        if side == "top_right":
                            bird.velocity_x, other_bird.velocity_x = other_bird.velocity_x, bird.velocity_x
                            bird.velocity_y, other_bird.velocity_y = other_bird.velocity_y, bird.velocity_y
                        if side == "bottom_left":
                            bird.velocity_x, other_bird.velocity_x = other_bird.velocity_x, bird.velocity_x
                            bird.velocity_y, other_bird.velocity_y = other_bird.velocity_y, bird.velocity_y
                        if side == "bottom_right":
                            bird.velocity_x, other_bird.velocity_x = other_bird.velocity_x, bird.velocity_x
                            bird.velocity_y, other_bird.velocity_y = other_bird.velocity_y, bird.velocity_y
                        #bird.velocity_x *= -1
                        #bird.velocity_y *= -1
                b += 1

                if bird.reached_screen_edge(self.screen_x,self.screen_y):
                    bird.bounce_off_edge(self.screen_x,self.screen_y)
                
                bird.move()                

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        for bird in self.bird_list:
            bird.draw()

        
App()