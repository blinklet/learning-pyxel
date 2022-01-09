import pyxel, time

pyxel.init(256, 256, quit_key=pyxel.KEY_Q, fps=2)
pyxel.load("assets/jump_game.pyxres")
direction = 1

def update():
    pass

def draw():
    pyxel.cls(0)
    if pyxel.frame_count % 2 == 0:
        direction = 1
    else:
        direction = -1
    pyxel.blt(128, 128, 0, 16, 0, 16 * direction, 16, 12)
    pyxel.text(1, 1, str(direction), 7)

pyxel.run(update, draw)
