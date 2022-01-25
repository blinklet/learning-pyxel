import pyxel
from random import randint


class Bird:
    def __init__(self, x, y, s):
        self.bird_x = x
        self.bird_y = y
        self.start_sprite = s
        self.bird_sprite_x = 0
        self.bird_sprite_y = 16

    def update(self):
        # Choose starting sprite, then animate across the three sprites
        self.bird_sprite_x = 8 * ((pyxel.frame_count + self.start_sprite) % 3)
        # Move bird and reset bird position if it moves off the screen
        self.bird_x = (self.bird_x + 1) % (pyxel.width + 8)
        self.bird_y = (self.bird_y - 1) % (pyxel.height + 8)

    def draw(self):
        pyxel.blt(self.bird_x, self.bird_y, 0, self.bird_sprite_x, self.bird_sprite_y, 8, 8, 2)


class App:
    def __init__(self):
        pyxel.init(32, 32, fps=2)
        pyxel.load("../assets/platformer.pyxres")
        self.bird1 = Bird(randint(0, pyxel.width), randint(0, pyxel.height), randint(0,2))
        self.bird2 = Bird(randint(0, pyxel.width), randint(0, pyxel.height), randint(0,2))
        # camera(8,8) creates an 8-pixel wide space on the top and left side of the 
        # screen that we can address without using negative numbers
        pyxel.camera(8, 8)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.bird1.update()
        self.bird2.update()

    def draw(self):
        pyxel.cls(0)
        self.bird1.draw()
        self.bird2.draw()

        
App()