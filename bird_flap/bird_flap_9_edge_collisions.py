import pyxel
from random import randint, choice

SCREEN_SIZE_X = 128
SCREEN_SIZE_Y = 64
OUTSIDE_SPACE_X = 0
OUTSIDE_SPACE_Y = 0
SPRITE_SIZE = 8
FPS = 12
BACKGROUND_COLOR = 2


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_sprite = randint(0,2)
        self.velocity_x = randint(-1, 1)
        if self.velocity_x == 0:
            self.velocity_y = choice([-1, 1]) # avoid motionless birds
        else:
            self.velocity_y = randint(-1, 1)
        self.image = 0
        self.sprite_size = SPRITE_SIZE
        self.transparent_color = 2
        self.sprite_location_x = 0
        self.sprite_location_y = 16
        self.facing = 1
        self.screen_x = pyxel.width + OUTSIDE_SPACE_X - self.sprite_size
        self.screen_y = pyxel.height + OUTSIDE_SPACE_Y - self.sprite_size

    def hit_border(self):
        if self.x == 0: 
            return True
        elif self.x == pyxel.width + OUTSIDE_SPACE_X - SPRITE_SIZE:
            return True
        elif self.y == 0:
            return True
        elif self.y == pyxel.height + OUTSIDE_SPACE_Y - SPRITE_SIZE:
            return True
        else:
            return False

    def update(self):
        # Choose starting sprite, then animate across the three sprites
        self.sprite_location_x = 8 * ((pyxel.frame_count + self.start_sprite) % 3)

        # bird faces right when moving right and left when moving left
        # but if it is only moving up or down, it faces right when going up 
        # and left when going down
        if self.velocity_x != 0:
            self.facing = self.velocity_x
        else:
            self.facing = self.velocity_y

        # change direction when bird reaches edge of screen, 
        if self.x <= 0 or self.x >= self.screen_x:
            self.velocity_x *= -1 
        if self.y <= 0 or self.y >= self.screen_y:
            self.velocity_y *= -1 

        # move bird
        self.x += self.velocity_x
        self.y -= self.velocity_y

    def draw(self):
        pyxel.blt(self.x, self.y, self.image, self.sprite_location_x, self.sprite_location_y, self.sprite_size * self.facing, self.sprite_size, self.transparent_color)


class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE_X, SCREEN_SIZE_Y, fps=FPS)
        pyxel.load("../assets/platformer.pyxres")
        self.bird_list = []
        # camera(8,8) creates an 8-pixel wide space on the top and left side of the 
        # screen that we can address without using negative numbers
        pyxel.camera(OUTSIDE_SPACE_X, OUTSIDE_SPACE_Y)
        pyxel.run(self.update, self.draw)

    # def edge_detected(sprite_list):
    #     if len(sprite_list) = 

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE):
            if len(self.bird_list) < 10:
                self.bird_list.append(Bird(randint(0, pyxel.width - SPRITE_SIZE - 1), randint(0, pyxel.height - SPRITE_SIZE - 1)))

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            if len(self.bird_list) > 0:
                self.bird_list.pop()

        for bird in self.bird_list:
            bird.update()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        for bird in self.bird_list:
            bird.draw()

        
App()