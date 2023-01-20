# Version 25

(done) changed the way FPS is used so that the "perceived FPS" is the movement rate of the Fastest sprint instead of the slowest

(done) changed logic so if SPRITE_SPEED = 0, game allows stationary sprite

(done)added walker sprite to game_sprites module

(done) added find_direction function to Sprite class

(done) Tried to fix jitter issue.
Solution works when bird = 1 and ball = 2 but fails for other ratios.

I think issue is due to floats. will try decimals in next version


Add walker at bottom of screen
  - Start game with "x" birds and 1 ball
  - if walker hit by bird, walker "catches" bird
    - bird disappears
    - new bird created
    - one more ball added
  - if walker hit by ball, ball rebounds and walker slows down -- making it harder to catch birds
Add score counter with timer and number of hits
