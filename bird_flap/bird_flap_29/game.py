import pyxel
import random
import itertools
import game_sprites
import inspect



SCREEN_SIZE_X = 150
SCREEN_SIZE_Y = 150
FPS = 30
# FPS must be higher than each sprite's SPRITE_FPS value. 
# The fastest sprite will appear to travel at the FPS speed.
# Every other sprite travels slower, 
# at (SPRITE_SPEED/MAX_SPRITE_SPEED)*FPS speed
BACKGROUND_COLOR = 2
ASSET_FILE = "../../assets/platformer.pyxres"
MAX_SPRITES_FACTOR = 0.45

# Get highest speed from classes defined in game_sprites module
def get_speed():
    speed_list = []
    for name, obj in inspect.getmembers(game_sprites):
        if inspect.isclass(obj):
            speed_list.append(int(inspect.getattr_static(obj,"SPRITE_SPEED")))
    return max(speed_list)

# Get largest sprite width from classes defined in game_sprites module
def get_width():
    width_list = []
    for name, obj in inspect.getmembers(game_sprites):
        if inspect.isclass(obj):
            width_list.append(int(inspect.getattr_static(obj,"SPRITE_WIDTH")))
    return max(width_list)

# Get largest sprite height from classes defined in game_sprites module
def get_height():
    height_list = []
    for name, obj in inspect.getmembers(game_sprites):
        if inspect.isclass(obj):
            height_list.append(int(inspect.getattr_static(obj,"SPRITE_HEIGHT")))
    return max(height_list)

LARGEST_SPRITE_WIDTH = get_width()
LARGEST_SPRITE_HEIGHT = get_height()
MAX_SPRITE_SPEED = get_speed()


clock_fps = FPS 
base_fps = pyxel.ceil(FPS / MAX_SPRITE_SPEED)

class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE_X, SCREEN_SIZE_Y, fps=clock_fps)
        pyxel.load(ASSET_FILE)
        self.sprite_list = []
        self.max_sprites = ((pyxel.width // LARGEST_SPRITE_WIDTH) * \
            (pyxel.height // LARGEST_SPRITE_HEIGHT)) * MAX_SPRITES_FACTOR
        self.walker_x = random.randint(1, pyxel.width - game_sprites.Walker1.SPRITE_WIDTH - 1)
        self.walker_y = pyxel.height - game_sprites.Walker1.SPRITE_HEIGHT
        self.hit = False
        self.walker = game_sprites.Walker1(self.walker_x, self.walker_y, MAX_SPRITE_SPEED, base_fps, self.hit)

        pyxel.run(self.update, self.draw)

    def generate_sprite(self, sprite_type):
        # Create new sprite in random position start with even-numbered points to smooth
        # diagonal motion at start (but does not ensure smooth diagonal motion after collision )
        if sprite_type == "bird":
            new_bird_x = random.randint(1, pyxel.width - game_sprites.Bird.SPRITE_WIDTH - 1)
            new_bird_y = random.randint(1, pyxel.height - game_sprites.Bird.SPRITE_HEIGHT - 17) # leave space for walker
            return(game_sprites.Bird(new_bird_x, new_bird_y, MAX_SPRITE_SPEED, base_fps))
        if sprite_type == "ball":
            new_ball_x = random.randint(1, pyxel.width - game_sprites.Ball.SPRITE_WIDTH - 1)
            new_ball_y = random.randint(1, pyxel.height - game_sprites.Ball.SPRITE_HEIGHT - 17)
            return(game_sprites.Ball(new_ball_x, new_ball_y, MAX_SPRITE_SPEED, base_fps))
        if sprite_type == "sprite":
            new_sprite_x = random.randint(1, pyxel.width - game_sprites.Sprite.SPRITE_WIDTH - 1)
            new_sprite_y = random.randint(1, pyxel.height - game_sprites.Sprite.SPRITE_HEIGHT - 1)
            return(game_sprites.Sprite(new_sprite_x, new_sprite_y, MAX_SPRITE_SPEED, base_fps))
        # if sprite_type == "walker":
        #     new_sprite_x = random.randint(1, pyxel.width - game_sprites.Walker1.SPRITE_WIDTH - 1)
        #     new_sprite_y = pyxel.height - game_sprites.Walker1.SPRITE_HEIGHT
        #     return(game_sprites.Walker1(new_sprite_x, new_sprite_y, MAX_SPRITE_SPEED, base_fps))

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

        if pyxel.btnp(pyxel.KEY_A, 1, 1) or pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
            self.walker.update("left")

        if pyxel.btnp(pyxel.KEY_F, 1, 1) or pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
            self.walker.update("right")                 

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.remove_sprite()

        # detect collisions and move birds.
        # itertools offers a way to do this. 
        # See https://stackoverflow.com/questions/16603282/how-to-compare-each-item-in-a-list-with-the-rest-only-once
        # for examples of various ways to compare items in a list (without multiple comparisons)
        # https://docs.python.org/3/library/itertools.html#itertools.combinations
        #
        # maybe try different approach: https://gamedev.net/forums/topic/701045-axis-aligned-rectangle-collision-handling/5400917/

        # Check screen or walker collision first (new velocity in bounce_off_edge function)
        # Check all birds for contact with edge and walker  
        for num, sprite in enumerate(self.sprite_list):
            if sprite.reached_screen_edge(pyxel.width,pyxel.height):
                #sprite.previous_collision_detected = True  # do not change direction after this collision, during this round
                # sprite.snap()
                sprite.bounce_off_edge(pyxel.width,pyxel.height)
            if sprite.intersects(self.walker):   # sprite hits walker
                self.walker.hit = True
                self.sprite_list.pop(num) 
                self.add_new_sprite(sprite.TYPE) # replace sprite somewhere else on the screen

     


        # for sprite, other_sprite in itertools.combinations(self.sprite_list, 2):
        #     if other_sprite.previous_collision_detected == False: 
        #         if sprite.intersects(other_sprite): 
        #             other_sprite.previous_collision_detected = True  # set collision flag on other birds where detected with current sprite
        #             # sprite.snap()
        #             # other_sprite.snap()
        #             sprite.velocity_x, other_sprite.velocity_x = other_sprite.velocity_x, sprite.velocity_x
        #             sprite.velocity_y, other_sprite.velocity_y = other_sprite.velocity_y, sprite.velocity_y

        # for sprite in self.sprite_list:
        #     sprite.previous_collision_detected = False  # reset collisions on all birds
        #     sprite.animate()
        #     sprite.update()

        for i in range(len(self.sprite_list) - 1, -1, -1):
            bi = self.sprite_list[i]
            bi.animate()
            bi.update()

            for j in range(i - 1, -1, -1):
                bj = self.sprite_list[j]
                if bi.intersects(bj):
                    bi.velocity_x, bj.velocity_x = bj.velocity_x, bi.velocity_x
                    bi.velocity_y, bj.velocity_y = bj.velocity_y, bi.velocity_y



        self.walker.animate()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        self.walker.draw()
        for sprite in self.sprite_list:
            sprite.draw()

        
App()