import pyxel
import random
import itertools
import game_sprites
import inspect
import math

# Get highest speed factor from defined game_sprites classes
def get_speed():
    speed_list = []
    for name, obj in inspect.getmembers(game_sprites):
        if inspect.isclass(obj):
            speed_list.append(int(inspect.getattr_static(obj,"SPRITE_SPEED")))
    return max(speed_list)

# Get largest sprite width from defined game_sprites classes
def get_width():
    width_list = []
    for name, obj in inspect.getmembers(game_sprites):
        if inspect.isclass(obj):
            width_list.append(int(inspect.getattr_static(obj,"SPRITE_WIDTH")))
    return max(width_list)

# Get largest sprite height from defined game_sprites classes
def get_height():
    height_list = []
    for name, obj in inspect.getmembers(game_sprites):
        if inspect.isclass(obj):
            height_list.append(int(inspect.getattr_static(obj,"SPRITE_HEIGHT")))
    return max(height_list)

SCREEN_SIZE_X = 60
SCREEN_SIZE_Y = 60
FPS = 10    # FPS must be higher than each sprite's
            # SPRITE_FPS value. 
            # The fastest sprite will appear to travel
            # at the FPS speed

ASSET_FILE = "../../assets/platformer.pyxres"
LARGEST_SPRITE_WIDTH = get_width()
LARGEST_SPRITE_HEIGHT = get_height()
MAX_SPRITES_FACTOR = 0.45
MAX_SPRITE_SPEED = get_speed()
BACKGROUND_COLOR = 2

clock_fps = FPS 
fps = math.ceil(FPS / MAX_SPRITE_SPEED)

class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE_X, SCREEN_SIZE_Y, fps=clock_fps)
        pyxel.load(ASSET_FILE)
        self.sprite_list = []
        self.max_sprites = ((pyxel.width // LARGEST_SPRITE_WIDTH) * \
            (pyxel.height // LARGEST_SPRITE_HEIGHT)) * MAX_SPRITES_FACTOR

        pyxel.run(self.update, self.draw)

    def generate_sprite(self, sprite_type):
        # Create new sprite in random position start with even-numbered points to smooth
        # diagonal motion at start (but does not ensure smooth diagonal motion after collision )
        if sprite_type == "bird":
            new_bird_x = random.randint(1, pyxel.width - game_sprites.Bird.SPRITE_WIDTH - 1)
            new_bird_y = random.randint(1, pyxel.height - game_sprites.Bird.SPRITE_HEIGHT - 1)
            return(game_sprites.Bird(new_bird_x, new_bird_y, MAX_SPRITE_SPEED, fps))
        if sprite_type == "ball":
            new_ball_x = random.randint(1, pyxel.width - game_sprites.Ball.SPRITE_WIDTH - 1)
            new_ball_y = random.randint(1, pyxel.height - game_sprites.Ball.SPRITE_HEIGHT - 1)
            return(game_sprites.Ball(new_ball_x, new_ball_y, MAX_SPRITE_SPEED, fps))
        if sprite_type == "sprite":
            new_sprite_x = random.randint(1, pyxel.width - game_sprites.Sprite.SPRITE_WIDTH - 1)
            new_sprite_y = random.randint(1, pyxel.height - game_sprites.Sprite.SPRITE_HEIGHT - 1)
            return(game_sprites.Sprite(new_sprite_x, new_sprite_y, MAX_SPRITE_SPEED, fps))

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

        # detect collisions and move birds.
        # itertools offers a way to do this. 
        # See https://stackoverflow.com/questions/16603282/how-to-compare-each-item-in-a-list-with-the-rest-only-once
        # for examples of various ways to compare items in a list (without multiple comparisons)
        # https://docs.python.org/3/library/itertools.html#itertools.combinations
        #
        # maybe try different approach: https://gamedev.net/forums/topic/701045-axis-aligned-rectangle-collision-handling/5400917/

        # Check screen collision first (new velocity in bounce_off_edge function)
        # Check all birds for contact with edge and  
        for sprite in self.sprite_list:
            if sprite.reached_screen_edge(pyxel.width,pyxel.height):
                sprite.previous_collision_detected = True  # do not change direction after this collision, during this round
                sprite.bounce_off_edge(pyxel.width,pyxel.height)

        for sprite, other_sprite in itertools.combinations(self.sprite_list, 2):
            if other_sprite.previous_collision_detected == False: 
                if sprite.intersects(other_sprite): 
                    other_sprite.previous_collision_detected = True  # set collision flag on other birds where detected with current sprite
                    sprite.velocity_x, other_sprite.velocity_x = other_sprite.velocity_x, sprite.velocity_x
                    sprite.velocity_y, other_sprite.velocity_y = other_sprite.velocity_y, sprite.velocity_y
        
        for sprite in self.sprite_list:
            sprite.previous_collision_detected = False  # reset collisions on all birds
            sprite.move()

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        for sprite in self.sprite_list:
            sprite.draw()

        
App()