import pyxel

class Bird:
    def __init__(self, x, y, index):
        self.bird_x = x
        self.bird_y = y
        self.bird_index = index
        self.bird_sprite_x = 0

    def update(self):

        def move(x, y):
            x = x + pyxel.rndi(-1,1)
            y = y + pyxel.rndi(-1,1)
            return x, y
        
        def animate(bx, indx):
            if indx > 2:
                indx = 0
            bx = 8 * indx
            indx += 1
            return bx, indx

        if pyxel.frame_count % 10 == 0:
            self.bird_sprite_x, self.bird_index = animate(self.bird_sprite_x, self.bird_index)
            self.bird_x, self.bird_y = move(self.bird_x, self.bird_y) 

    def draw(self):
        pyxel.blt(self.bird_x, self.bird_y, 0, self.bird_sprite_x, 16, 8, 8, 2)


class App:
    def __init__(self):
        pyxel.init(64, 32, fps=30)
        pyxel.load("platformer.pyxres")
        self.bird_list = []
        for i in range(12):
            a = pyxel.rndi(0,56)
            b = pyxel.rndi(0,24)
            c = pyxel.rndi(0,2)
            self.bird_list.append(Bird(a, b, c))
        pyxel.run(self.update, self.draw)

    def update(self):
        for i in range(12):
            self.bird_list[i].update()

    def draw(self):
        pyxel.cls(6)
        for i in range(12):
            self.bird_list[i].draw()

App()