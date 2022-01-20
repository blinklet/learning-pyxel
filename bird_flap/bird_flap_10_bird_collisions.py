import pyxel
import random

SCREEN_SIZE_X = 50
SCREEN_SIZE_Y = 15
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

        self.is_same_bird = False
        self.start_sprite = random.randint(0,2)  # each bird starts at a random point in the sprite animation
        
        self.velocity_x = random.randint(-1, 1)  # each bird starts with a randomly-selected velocity (direction)
        if self.velocity_x == 0:
            self.velocity_y = random.choice([-1, 1]) # avoid motionless birds
        else:
            self.velocity_y = random.randint(-1, 1)

        self.facing = 1    # each bird starts facing left or right, depending on velocity on x axis

    def hit_border(self):
        if self.x == 0: 
            return True
        elif self.x == pyxel.width + OUTSIDE_SCREEN_SPACE_X - self.w:
            return True
        elif self.y == 0:
            return True
        elif self.y == pyxel.height + OUTSIDE_SCREEN_SPACE_Y - self.h:
            return True
        else:
            return False

    # Copied intersects function from https://github.com/CaffeinatedTech/Python_Nibbles/blob/master/main.py
    def intersects(self, other_x, other_y, other_w, other_h):
        is_intersected = False
        if (
            other_x + other_w > self.x
            and self.x + self.w > other_x
            and other_y + other_h > self.y
            and self.y + self.h > other_y
        ):
            is_intersected = True
        return is_intersected

    def collided(self):
        pass

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
        pyxel.load("../assets/platformer.pyxres")
        self.screen_x = pyxel.width + OUTSIDE_SCREEN_SPACE_X - BIRD_WIDTH
        self.screen_y = pyxel.height + OUTSIDE_SCREEN_SPACE_Y - BIRD_HEIGHT
        self.bird_list = []
        self.max_birds = ((pyxel.width // BIRD_WIDTH) * (pyxel.height // BIRD_HEIGHT))
        
        # camera(8,8) creates an 8-pixel wide space on the top and left side of the 
        # screen that we can address without using negative numbers
        pyxel.camera(OUTSIDE_SCREEN_SPACE_X, OUTSIDE_SCREEN_SPACE_Y)
        
        pyxel.run(self.update, self.draw)

    # Copied check_collisions function from https://github.com/CaffeinatedTech/Python_Nibbles/blob/master/main.py
    def check_collisions(self, bird):
        if self.apple.intersects(self.snake[0].x, self.snake[0].y, self.snake[0].w, self.snake[0].h):
            pass

    def add_new_bird(self):
        new_bird_x = random.randint(2, pyxel.width - BIRD_WIDTH - 2)
        new_bird_y = random.randint(2, pyxel.height - BIRD_HEIGHT - 2)

        counter = 0
        if len(self.bird_list) > 0:
            try_again = True
            while counter < 10 and try_again:
                try_again = False
                for bird in self.bird_list:
                    if bird.intersects(new_bird_x,new_bird_y,8,8):
                        try_again = True
                        new_bird_x = random.randint(2, pyxel.width - BIRD_WIDTH - 2)
                        new_bird_y = random.randint(2, pyxel.height - BIRD_HEIGHT - 2)
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

        for bird in self.bird_list:
            x_change = False
            y_change = False
            
            # change direction when bird reaches edge of screen, 
            if bird.x <= 1 or bird.x >= self.screen_x - 1:
                bird.velocity_x *= -1
                x_change = True

            if bird.y <= 1 or bird.y >= self.screen_y -1:
                bird.velocity_y *= -1
                y_change = True

            if x_change or y_change:
                bird.move()
                continue

            # Tag current bird so it does not check for collision with itself
            bird.is_same_bird = True
            
            # change direction when bird collides with another bird
            for other_bird in self.bird_list:
                if not other_bird.is_same_bird:
                    if bird.intersects(other_bird.x,other_bird.y,8,8):
                        if (bird.velocity_x == 1) or (bird.velocity_x == -1):
                            bird.velocity_x *= -1
                            if (other_bird.velocity_x == 1) or (other_bird.velocity_x == -1):
                                other_bird.velocity_x *= -1
                                other_bird.move()
                        if (bird.velocity_y == -1) or (bird.velocity_y == 1):
                            bird.velocity_y *= -1
                            if (other_bird.velocity_y == 1) or (other_bird.velocity_y == -1):
                                other_bird.velocity_y *= -1
                                other_bird.move()
                            

            bird.is_same_bird = False  # reset same_bird flag
            bird.move()
            # if x_change:
            #     bird.velocity_x *= -1
            
            # if y_change:
            #     bird.velocity_y *= -1

            # if x_change or y_change:
            #     bird.move()
                

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        for bird in self.bird_list:
            bird.draw()

        
App()