import pyxel
from sprites import Sprite

class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
 
        self.sprite_list = []
        for _ in range(12):
            self.sprite_list.append(Sprite())

        pyxel.run(self.update, self.draw)

    def update(self):
        for i in range(12):
            self.sprite_list[i].update()

    def draw(self):
        pyxel.cls(6)
        for i in range(12):
            self.sprite_list[i].draw()

App()