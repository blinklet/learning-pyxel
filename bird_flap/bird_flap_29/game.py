import pyxel
import game_sprites
import inspect


SCREEN_SIZE_X = 100
SCREEN_SIZE_Y = 100
FPS = 30
# FPS must be higher than each sprite's SPRITE_FPS value. 
# The fastest sprite will appear to travel at the FPS speed.
# Every other sprite travels slower, 
# at (SPRITE_SPEED/MAX_SPRITE_SPEED)*FPS speed
BACKGROUND_COLOR = 2
ASSET_FILE = "../../assets/platformer.pyxres"
MAX_SPRITES_FACTOR = 0.45

# Get highest speed from classes defined in game_sprites module
def fastest_sprite_speed():
    speed_list = []
    for name, obj in inspect.getmembers(game_sprites):
        if inspect.isclass(obj):
            speed_list.append(int(inspect.getattr_static(obj,"SPRITE_SPEED")))
    return max(speed_list)

# Get largest sprite width from classes defined in game_sprites module
def largest_sprite_width():
    width_list = []
    for name, obj in inspect.getmembers(game_sprites):
        if inspect.isclass(obj):
            width_list.append(int(inspect.getattr_static(obj,"SPRITE_WIDTH")))
    return max(width_list)

# Get largest sprite height from classes defined in game_sprites module
def largest_sprite_height():
    height_list = []
    for name, obj in inspect.getmembers(game_sprites):
        if inspect.isclass(obj):
            height_list.append(int(inspect.getattr_static(obj,"SPRITE_HEIGHT")))
    return max(height_list)


clock_fps = FPS 
base_fps = pyxel.ceil(FPS / fastest_sprite_speed())

class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE_X, SCREEN_SIZE_Y, fps=clock_fps)
        pyxel.load(ASSET_FILE)
        self.sprite_list = []
        self.max_sprites = ((pyxel.width // largest_sprite_width()) * \
            (pyxel.height // largest_sprite_height())) * MAX_SPRITES_FACTOR
        self.hit = False
        self.walker = game_sprites.Walker1(fastest_sprite_speed(), base_fps, self.hit)

        pyxel.run(self.update, self.draw)

    def generate_sprite(self, sprite_type):
        if sprite_type == "bird":
            return(game_sprites.Bird(fastest_sprite_speed(), base_fps))
        if sprite_type == "ball":
            return(game_sprites.Ball(fastest_sprite_speed(), base_fps))
        if sprite_type == "sprite":
            return(game_sprites.Sprite(fastest_sprite_speed(), base_fps))

    def add_new_sprite(self, sprite_type):
        # Create new sprite in random position
        new_sprite = self.generate_sprite(sprite_type)

        # Check if new sprite object overlaps or collides with any existing sprite
        counter = 0
        if len(self.sprite_list) > 0:
            try_again = True
            while counter < 10 and try_again:
                try_again = False
                for sprite in self.sprite_list:
                    if sprite.intersects(new_sprite):
                        try_again = True
                        new_sprite = self.generate_sprite(sprite_type)   # new sprite in new random location
                        break   # no need to continue after first collision found
                if try_again == True:
                    print(f'{counter} - No space')
                    counter += 1
        
        # if the loop ran ten times without finding free space for a new sprite, do nothing
        if counter < 10:
            self.sprite_list.append(new_sprite)

    def remove_sprite(self):
        if len(self.sprite_list) > 0:
            self.sprite_list.pop()

    def at_max_sprites(self):
        if len(self.sprite_list) >= self.max_sprites:
            print("Maximum sprites reached")
            return True
        else:
            return False

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_B):
            if not self.at_max_sprites():
                self.add_new_sprite("bird")

        if pyxel.btnp(pyxel.KEY_V):
            if not self.at_max_sprites():
                self.add_new_sprite("ball")

        if pyxel.btnp(pyxel.KEY_T):
            if not self.at_max_sprites():
                self.add_new_sprite("sprite")              

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.remove_sprite()

        self.walker.animate()
        self.walker.update()

        for i in range(len(self.sprite_list) - 1, -1, -1):
            bi = self.sprite_list[i]
            bi.animate()
            bi.update()

            for j in range(i - 1, -1, -1):
                bj = self.sprite_list[j]
                if bi.intersects(bj):
                    bi.velocity_x, bj.velocity_x = bj.velocity_x, bi.velocity_x
                    bi.velocity_y, bj.velocity_y = bj.velocity_y, bi.velocity_y

            if bi.intersects(self.walker):   # sprite hits walker
                self.walker.hit = True
                del self.sprite_list[i]
                self.add_new_sprite(bi.TYPE) 

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        self.walker.draw()
        for sprite in self.sprite_list:
            sprite.draw()

        
App()