import pyxel, time

pyxel.init(256, 256, quit_key=pyxel.KEY_Q)
pyxel.cls(0)
pyxel.load("assets/jump_game.pyxres")

while True:
    pyxel.blt(128, 128, 0, 16, 0, 16, 16, 12)
    time.sleep(1)
    pyxel.flip()
    pyxel.blt(128, 128, 0, 16, 0, -16, 16, 12)
    time.sleep(1)
    pyxel.flip()