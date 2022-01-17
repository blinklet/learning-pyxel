import pyxel

class App:
    def __init__(self):
        pyxel.init(64, 32, fps=2)
        pyxel.load("../assets/platformer.pyxres")
        self.bird_x = 28
        self.bird_y = 12
        self.bird_sprite_x = 0
        self.bird_sprite_y = 16
        pyxel.run(self.update, self.draw)

    def update(self):
        self.bird_sprite_x = 8 * (pyxel.frame_count % 3)

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(self.bird_x, self.bird_y, 0, self.bird_sprite_x, self.bird_sprite_y, 8, 8, 2)

App()