import pyxel

pyxel.init(128, 128, fps=6)
pyxel.load("assets/platformer.pyxres")
direction = 1
bird_frame = 0

def update():
    global bird_frame
    bird_frame = 8 * (pyxel.frame_count % 3)
    print(bird_frame)

def draw():
    global bird_frame
    pyxel.cls(0)
    pyxel.blt(60, 60, 0, bird_frame, 16, 8, 8, 2)
    pyxel.text(1, 1, str(bird_frame), 7)

pyxel.run(update, draw)
