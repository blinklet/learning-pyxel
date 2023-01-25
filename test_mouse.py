import pyxel

pyxel.init( 80 , 64 )
pyxel.load( "assets/jump_game.pyxres" )

x = 0 
y = 0 
def update ():
    global x,y
    x = pyxel.mouse_x
    y = pyxel.mouse_y
    print(x,y)
    return

def draw ():
    pyxel.cls( 1 )
    pyxel.blt( 5 , 5 , 0 , 8 , 0 , 8 , 8 , 0 )
    pyxel.blt( x, y, 0 , 8 , 0 , 8 , 8 , 0 )
    return

pyxel.run(update,draw)