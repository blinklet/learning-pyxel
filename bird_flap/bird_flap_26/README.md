# Version 25


Fix jitter solution
I think issue is due to floats. will try decimals in next version

Tried addiong partial distances when jitter is detected so that eventaully the x and y are in sync

but seemed to cause more sprites sticking to each other

Should go back to rounding solution
but how to solve the cycle of bad jitter detections?


(maybe remove jitter logic until future and focu on other game mechanics)

Add walker at bottom of screen
  - Start game with "x" birds and 1 ball
  - if walker hit by bird, walker "catches" bird
    - bird disappears
    - new bird created
    - one more ball added
  - if walker hit by ball, ball rebounds and walker slows down -- making it harder to catch birds
Add score counter with timer and number of hits
