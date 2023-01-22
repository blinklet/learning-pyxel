# Version 27

Problem: walker moves x pixels per key press, where x = walker speed value
   regardless of speed ratio of other sprites
   need to make walker move according to speed ratio but also allow mechanism to change walker's speed in game due to ball collisions
   (fixed)

Problem: snap function increase probablity of stuck sprites
(done) just stop working on jitter issue. Comment out snap function calls

(done) Moved walkere animate from update functiomn to section where I animare other sprotes

(done) walker changes color when hit, sprite disappears, new sprite gets created



Add walker at bottom of screen
  - Start game with "x" birds and 1 ball
  - if walker hit by bird, walker "catches" bird
    - bird disappears
    - new bird created
    - one more ball added
  - if walker hit by ball, ball rebounds and walker slows down -- making it harder to catch birds
Add score counter with timer and number of hits
