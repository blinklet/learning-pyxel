import pyxel

pyxel.init(128, 128, fps=2)
pyxel.load("assets/platformer.pyxres")
bird_sprite_x = 0
bird_sprite_y = 16

def update():
    pass

def draw():
    pyxel.cls(0)
    bird_sprite_x = 8 * (pyxel.frame_count % 3)
    pyxel.blt(60, 60, 0, bird_sprite_x, bird_sprite_y, 8, 8, 2)

pyxel.run(update, draw)
