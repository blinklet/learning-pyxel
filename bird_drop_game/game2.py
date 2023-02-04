import pyxel
from sprites2 import Sprite


class Ball(Sprite):
    def __init__(self):
        super().__init__()
        self.w = 6
        self.h = 6
        self.animation = ((1, 9), (9, 9), (17, 9))
        self.animation_index = pyxel.rndi(0,len(self.animation))

class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
 
        self.sprite_list = []
        for _ in range(6):
            self.sprite_list.append(Sprite())
            self.sprite_list.append(Ball())           
        print(self.sprite_list)
        pyxel.run(self.update, self.draw)

    def update(self):
        for i in range(12):
            self.sprite_list[i].update()

    def draw(self):
        pyxel.cls(6)
        for i in range(12):
            self.sprite_list[i].draw()

App()