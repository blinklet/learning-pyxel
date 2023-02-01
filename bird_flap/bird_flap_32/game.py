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
BACKGROUND_COLOR = 6
BACKGROUND_FLASH = [8, 8, 10, 10, 8, 8]
ASSET_FILE = "../../assets/platformer.pyxres"
MAX_SPRITES_FACTOR = 0.15
SPRITE_INTERVAL = 60



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
        self.max_sprites = int(((pyxel.width / largest_sprite_width()) * \
            (pyxel.height / largest_sprite_height())) * MAX_SPRITES_FACTOR)
        self.flash_red = False
        self.walker = game_sprites.Walker1(fastest_sprite_speed(), base_fps, self.flash_red)
        self.score = 0
        self.lives_left = 3
        self.flash_count = 0
        self.background_color = BACKGROUND_COLOR
        self.GAME_OVER = False
        self.START_SCREEN = True
        pyxel.playm(0, loop=True)
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

    def update_game(self):

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.frame_count % SPRITE_INTERVAL == 0:
            if not self.at_max_sprites():
                self.add_new_sprite("bird")

        if pyxel.frame_count % (3 * SPRITE_INTERVAL) == 0:
            if not self.at_max_sprites():
                self.add_new_sprite("ball")

        self.walker.animate()
        self.walker.update()

        # collision detection algorithm copied from pyxel_examples/09_shooter.py
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
                del self.sprite_list[i]
                self.walker.hit = True
                if bi.TYPE == "bird":
                    pyxel.play(3, 8)  # channel 3 because it is not used for anything else
                    self.score = self.score + 1
                    self.flash_red = False
                else:
                    pyxel.play(3, 9)
                    self.flash_red = True
                    self.flash_count = 0
                    self.score = self.score - 1
                    if self.score < 0:
                        self.score = 0
                    self.lives_left = self.lives_left - 1
                    if self.lives_left <= 0:
                        self.lives_left = 0  
                        self.GAME_OVER = True

        if self.flash_red:
            self.background_color = BACKGROUND_FLASH[self.flash_count]
            self.flash_count = self.flash_count + 1
            if self.flash_count == len(BACKGROUND_FLASH):
                self.flash_red = False
                self.flash_count = 0
        else:
            self.background_color = BACKGROUND_COLOR

    def update_start_screen(self):
        if pyxel.btnp(pyxel.KEY_S):
            self.START_SCREEN = False
            self.sprite_list = []
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.walker.animate()
        if not self.sprite_list:
            self.add_new_sprite("bird")
            self.add_new_sprite("bird")
            self.sprite_list[0].y = pyxel.rndi(10, pyxel.height // 2 - 14)
            self.sprite_list[1].y = pyxel.rndi(10, pyxel.height // 2 - 14)

    def update_end_screen(self):
        if pyxel.btnp(pyxel.KEY_S):
            self.GAME_OVER = False
            self.sprite_list = []
            self.flash_red = False
            self.score = 0
            self.lives_left = 3
            self.flash_count = 0
            self.background_color = BACKGROUND_COLOR
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def update(self):
        if self.START_SCREEN:
            self.update_start_screen()
        elif self.GAME_OVER:
            self.update_end_screen()
        else:
            self.update_game()

    def draw_start_screen(self):
        pyxel.cls(2)
        pyxel.rect(0, pyxel.height - 6, pyxel.width, 6, 3) # Draw a rectangle of width w, height h and color col from (x, y).
        self.walker.draw()
        message = "Press S key"
        pyxel.text(pyxel.width // 2 - len(message) // 2 * 4, pyxel.height // 2, message, 7)
        message2 = "to start"
        pyxel.text(pyxel.width // 2 - len(message2) // 2 * 4, pyxel.height // 2 + 6, message2, 7)

        for sprite in self.sprite_list:
            sprite.draw()

    def draw_end_screen(self):
        pyxel.cls(10)
        pyxel.rect(0, pyxel.height - 6, pyxel.width, 6, 3) # Draw a rectangle of width w, height h and color col from (x, y).
        self.walker.draw()
        for sprite in self.sprite_list:
            sprite.draw()
        message = "GAME OVER"
        pyxel.text(pyxel.width//2 - len(message) // 2 * 4, pyxel.height // 2 - 12, message, 7)
        message2 = "Press S key"
        pyxel.text(pyxel.width//2 - len(message2) // 2 * 4, pyxel.height // 2 + 6, message2, 7)
        message3 = "to restart"
        pyxel.text(pyxel.width//2 - len(message3) // 2 * 4, pyxel.height // 2 + 12, message3, 7)
        pyxel.text(5, 5, "SCORE: " + str(self.score), 7)
        pyxel.text(pyxel.width - 36, 5, "LIVES: 0", 7)

    def draw_game(self):
        pyxel.cls(self.background_color)
        pyxel.rect(0, pyxel.height - 6, pyxel.width, 6, 3) # Draw a rectangle of width w, height h and color col from (x, y).
        self.walker.draw()
        for sprite in self.sprite_list:
            sprite.draw()
        pyxel.text(5, 5, "SCORE: " + str(self.score), 7)
        pyxel.text(pyxel.width - 36, 5, "LIVES: " + str(self.lives_left), 7)

    def draw(self):
        if self.START_SCREEN:
            self.draw_start_screen()
        elif self.GAME_OVER:
            self.draw_end_screen()
        else:
            self.draw_game()

        
App()