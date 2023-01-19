# Version 21

(done) Fix animation flow for various speeds

(done) Change collision logic so it does not use speed. Just use +1 to detect collisions

(done) generalize animation cycle in move functions

(done) Also need to change the way I calculate screen size for different-sized sprites
Right now, I always assume sprite is 8 pixels so if a sprite that is 6 pixels hits right or bottom of screen, it stops 2 pixels short!

(done) fixed calculations about frame rate and game clock so we get expected behavior
  now, the perceived movement speed is the same as teh FPS constant and separate from the actual game frame rate (which is FPS * max sprite speed)
  also, velocities are now relevant to the fasted sprite speed
    example: fastest sprite with speed 3 = 1.0 moves per Frame, or equals the perceived frame rate (FPS variable)
             other sprite with speed 1 = 1/3 or 0.33333 per Frame
          really, the fastest rate in this example appears to move three times in three frames, then the slower sprite moves once in three frames