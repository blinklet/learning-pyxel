# Version 24

(done)Generalize "move" function in sprites so it can be moved back to sprite.Sprite
There is only one line to change
replace it with pre-calculated animation sequence numbers

(done) More cleanup of sprite instance variables in game_sprites module

(done) removed the logic in game.py about setting space outside the boundary using the pyxel.camera method
       this is currently not being used and it creates unnecessary code
       
Add walker at bottom of screen
  - Start game with "x" birds and 1 ball
  - if walker hit by bird, walker "catches" bird
    - bird disappears
    - new bird created
    - one more ball added
  - if walker hit by ball, ball rebounds and walker slows down -- making it harder to catch birds
Add score counter with timer and number of hits
