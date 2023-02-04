import pyxel

class Sprite:
    def __init__(self):
        self.x = pyxel.rndi(0,56)
        self.y = pyxel.rndi(0,24)
        self.w = 8
        self.h = 8
        self.col = 2
        self.animate_interval = 10
        self.move_interval = 25
        self.animation = ((16, 16), (0, 16), (8, 16), (0, 16))
        self.animation_index = pyxel.rndi(0,len(self.animation))

    def move(self):
        if pyxel.frame_count % self.move_interval == 0:
            self.x += pyxel.rndi(-1,1)
            self.y += pyxel.rndi(-1,1)
    
    def animate(self):
        if pyxel.frame_count % self.animate_interval == 0:
            if self.animation_index == len(self.animation):
                self.animation_index = 0
            self.u, self.v = self.animation[self.animation_index]
            self.animation_index += 1

    def update(self):
        self.animate()
        self.move() 

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h, self.col)