import pyxel

class Bird:
    def __init__(self, x, y, index):
        self.bird_x = x
        self.bird_y = y
        self.bird_index = index

    def update(self):
        if pyxel.frame_count % 10 == 0:
            if self.bird_index > 2:
                self.bird_index = 0
            self.bird_sprite_x = 8 * self.bird_index
            self.bird_index += 1

    def draw(self):
        pyxel.blt(self.bird_x, self.bird_y, 0, self.bird_sprite_x, 16, 8, 8, 2)


class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
        self.bird1 = Bird(6,6,0)
        self.bird2 = Bird(28,12,1)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.bird1.update()
        self.bird2.update()

    def draw(self):
        pyxel.cls(6)
        self.bird1.draw()
        self.bird2.draw()

App()