# Version 25

(done) changed the way FPS is used so that the "perceived FPS" is the movement rate of the Fastest sprint instead of the slowest

(done) changed logic so if SPRITE_SPEED = 0, game allows stationary sprite

Add walker at bottom of screen
  - Start game with "x" birds and 1 ball
  - if walker hit by bird, walker "catches" bird
    - bird disappears
    - new bird created
    - one more ball added
  - if walker hit by ball, ball rebounds and walker slows down -- making it harder to catch birds
Add score counter with timer and number of hits
