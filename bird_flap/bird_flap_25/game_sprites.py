from sprite import Sprite


class Bird(Sprite):
    SPRITE_WIDTH = 8
    SPRITE_HEIGHT = 8
    SPRITE_SPEED = 1
    SPRITE_FPS = 3            # animation frame rate
    def __init__(self, x, y, fastest_sprite_speed, game_fps):
        Sprite.__init__(self, x, y, fastest_sprite_speed, game_fps)
        self.sequence = ((0, 16),(8, 16), (16, 16), (8, 16))  # x-coordinates of sprite animation frames
        self.animation_size = len(self.sequence) - 1
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file

class Ball(Sprite):
    SPRITE_WIDTH = 6
    SPRITE_HEIGHT = 6
    SPRITE_SPEED = 2
    SPRITE_FPS = 2            # animation frame rate
    def __init__(self, x, y, fastest_sprite_speed, game_fps):
        Sprite.__init__(self, x, y, fastest_sprite_speed, game_fps)
        self.sequence = ((17, 33), (25, 33))  # x-coordinates of sprite animation frames
        self.animation_size = len(self.sequence) - 1
        self.u = self.sequence[0][0]  # initial sprite horizontal position in image in resource file
        self.v = self.sequence[0][1]  # initial sprite vertical position in image in resource file

#__all__ = ["Ball", "Bird"]
