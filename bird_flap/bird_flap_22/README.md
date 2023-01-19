# Version 22

(done) made animations slower by adding more elements to each sprite's animation sequence

(done) previously made mistakes in calculations about frame rate vs FPS
turns out I was dividing by max sprite speed twice
(perils of using class variables instead of explicitly passing in parameters)
with that changes (see commented-out lines in generate_sprite function in game.py file) perceived frame rate is (max-sprite-speed * FPS)
so game speeds up when FPS is increased 
and sprite perceived FPS = the sprite speed

(done)another problem with the animation is my logic was squaring the length of the animation because I was calculating the loop size according to list length then going through the list "length" times in each iteration
    The game speed, clock_fps = FPS * MAX_SPRITE_SPEED
    "perceived speed" = FPS
    Slowest sprite moves once each perceived tick of FPS
    Animation should run one frame per perceived tick of FPS
    move function has access to both FPS and MAX_SPRITE_SPEED
    (change relative animation speed by doubling length of animation sequence)
    (speed of animation is proportional to FPS (higher = faster) and length of animation sequence (longer = slower))
    (speed of animation does not change if MAX_SPRITE_SPEED or sprite speed changes)
    maybe add some automatic sequence lengthener for higher FPS
    sat I want animation to run every 1/4 second on average
    If FPS = 20, animation should run ever 5 Fs.

        FPS = 10
        MAX_SPRITE_SPEED + 2 (from ball)
        clock_fps = 20

        Bird:
        SPEED = 1
        ANIMATION_LENGTH = 4
        V = 0.5
        (need to run one frame every two clocks because MAX_SPRITE_SPEED = 2)

        Ball:
        SPEED = 2
        ANIMATION_LENGTH = 4
        V = 1
        (need to run one frame every two clocks because MAX_SPRITE_SPEED = 2)


Fix jitter in sprite movement
issue is sawtooth pattern of diagonal movement due to rounding
Try to arrange so that pairs of values for slower objects match each other
for example, when fastest object is speed=2, an object with speed=1 should:
           (13.0,51.0)(13.5,50.5)(14.0,50.0)(14.5,49.5)
instead of (13,  51  )(14,  51  )(14,  50  )(15,  50  )
need       (13,  51  )(13,  51  )(14,  50  )(14,  50  )

int(abs(13.0)) - abs(13.5) = 0.5
int(abs(13.5)) - abs(14.0) = 1.0
int(abs(14.0)) - abs(14.5) = 0.5
int(abs(14.5)) - abs(15.0) = 1.0

int(abs(13.0)) - abs(13.33) = 0.33
int(abs(13.33)) - abs(13.67) = 0.67
int(abs(13.67)) - abs(14.0) = 1.0
int(abs(14.0)) - abs(14.33) = 0.33
int(abs(14.33)) - abs(14.67) = 0.67
int(abs(14.67)) - abs(15.0) = 1.0

abs(13.0)) - int(abs(13.5)) = 0
abs(13.5)) - int(abs(14.0)) = 0.5
abs(14.0)) - int(abs(14.5)) = 0
abs(14.5)) - int(abs(15.0)) = 0.5

abs(13.0) - int(abs(13.33)) = 0
abs(13.33) - int(abs(13.67)) = 0.33
abs(13.67) - int(abs(14.0)) = 0.67
abs(14.0) - int(abs(14.33)) = 0
abs(14.33) - int(abs(14.67)) = 0.33
abs(14.67) - int(abs(15.0)) = 0.67
