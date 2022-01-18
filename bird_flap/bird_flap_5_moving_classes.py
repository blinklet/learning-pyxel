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
        self.bird_x += 1
        if self.bird_x > pyxel.width:
            self.bird_x = -8
        self.bird_y -= 1
        if self.bird_y < -8:
            self.bird_y = pyxel.height

    def draw(self):
        pyxel.blt(self.bird_x, self.bird_y, 0, self.bird_sprite_x, self.bird_sprite_y, 8, 8, 2)


class App:
    def __init__(self):
        pyxel.init(64, 32, fps=2)
        pyxel.load("../assets/platformer.pyxres")
        self.bird1 = Bird(8,8,randint(0,2))
        self.bird2 = Bird(16,16,randint(0,2))
        pyxel.run(self.update, self.draw)

    def update(self):
        self.bird1.update()
        self.bird2.update()

    def draw(self):
        pyxel.cls(0)
        self.bird1.draw()
        self.bird2.draw()

        
App()