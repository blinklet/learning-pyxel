# Version 27
(not needed) Refactor so each class has an update and a draw method

(done) New collision algorithm (copied from click game example)
------------------
Go through spritelist backwards:
    ts = this sprite
    update x (includes wall collision check)
    Go through list starting at this sprite, backwards
        os = this other sprite
        check if ts and os intersect, if so:
            collision logic
This seems to work. Slightly less stuck birds and simpler logic

Change hit box on sprites to circles?



Add walker at bottom of screen
  - Start game with "x" birds and 1 ball
  - if walker hit by bird, walker "catches" bird
    - bird disappears
    - new bird created
    - one more ball added
  - if walker hit by ball, ball rebounds and walker slows down -- making it harder to catch birds
Add score counter with timer and number of hits
