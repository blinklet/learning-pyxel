import pyxel
from random import randint

SCREEN_SIZE_X = 32
SCREEN_SIZE_Y = 32
OUTSIDE_SPACE_X = 0
OUTSIDE_SPACE_Y = 0
FPS = 6

class Bird:
    def __init__(self, x, y, s):
        self.x = x
        self.y = y
        self.start_sprite = s
        self.image = 0
        self.sprite_size = 8
        self.transparent_color = 2
        self.sprite_location_x = 0
        self.sprite_location_y = 16
        self.facing = 1
        self.screen_x = pyxel.width + OUTSIDE_SPACE_X
        self.screen_y = pyxel.height + OUTSIDE_SPACE_Y

    def update(self):
        # Choose starting sprite, then animate across the three sprites
        self.sprite_location_x = 8 * ((pyxel.frame_count + self.start_sprite) % 3)
        # Move bird and reset bird position if it moves off the screen
        self.x = (self.x + 1) % self.screen_x
        self.y = (self.y - 1) % self.screen_y

    def draw(self):
        pyxel.blt(
            self.x, 
            self.y, 
            self.image, 
            self.sprite_location_x, 
            self.sprite_location_y, 
            self.sprite_size * self.facing, 
            self.sprite_size, 
            self.transparent_color
        )


class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE_X, SCREEN_SIZE_Y, fps=FPS)
        pyxel.load("../assets/platformer.pyxres")
        self.bird_list = []
        # camera(8,8) creates an 8-pixel wide space on the top and left side of the 
        # screen that we can address without using negative numbers
        pyxel.camera(OUTSIDE_SPACE_X, OUTSIDE_SPACE_Y)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_SPACE):
            if len(self.bird_list) < 11:
                self.bird_list.append(Bird(randint(0, pyxel.width), randint(0, pyxel.height), randint(0,2)))
        if pyxel.btn(pyxel.KEY_BACKSPACE):
            if len(self.bird_list) > 0:
                self.bird_list.pop()
        for bird in self.bird_list:
            bird.update()

    def draw(self):
        pyxel.cls(0)
        for bird in self.bird_list:
            bird.draw()

        
App()