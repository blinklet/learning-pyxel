import pyxel

pyxel.init(120, 80, fps=10)

while True:
    pyxel.cls(11)
    pyxel.rectb(pyxel.frame_count % 160 - 40, 20, 40, 40, 7)
    pyxel.flip()