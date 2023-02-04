import pyxel

class Sprite:
    def __init__(self):
        self.x = pyxel.rndi(0,56)
        self.y = pyxel.rndi(0,24)
        self.w = 6
        self.h = 6
        self.col = 2
        self.animation = ((1, 9), (9, 9), (17, 9))
        self.animation_index = pyxel.rndi(0,len(self.animation))

    def move(self):
        if pyxel.frame_count % 25 == 0:
            self.x += pyxel.rndi(-1,1)
            self.y += pyxel.rndi(-1,1)
    
    def animate(self):
        if pyxel.frame_count % 10 == 0:
            if self.animation_index == len(self.animation):
                self.animation_index = 0
            self.u, self.v = self.animation[self.animation_index]
            self.animation_index += 1

    def update(self):
        self.animate()
        self.move() 

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h, self.col)

class Egg(Sprite):
    def __init__(self):
        Sprite.__init__(self)

class Bird(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.w = 8
        self.h = 8
        self.animation = ((16, 16), (0, 16), (8, 16), (0, 16))
        self.animation_index = pyxel.rndi(0,len(self.animation))

class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
 
        self.sprite_list = []
        for _ in range(6):
            self.sprite_list.append(Bird())
            self.sprite_list.append(Egg())

        pyxel.run(self.update, self.draw)

    def update(self):
        for i in range(12):
            self.sprite_list[i].update()

    def draw(self):
        pyxel.cls(6)
        for i in range(12):
            self.sprite_list[i].draw()

App()