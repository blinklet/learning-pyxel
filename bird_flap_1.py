import pyxel

pyxel.init(64, 32, fps=2)
pyxel.load("assets/platformer.pyxres")
bird_x = 28
bird_y = 28
bird_sprite_x = 0
bird_sprite_y = 16

def update():
    pass

def draw():
    pyxel.cls(0)
    bird_sprite_x = 8 * (pyxel.frame_count % 3)
    pyxel.blt(bird_x, bird_y, 0, bird_sprite_x, bird_sprite_y, 8, 8, 2)

pyxel.run(update, draw)
