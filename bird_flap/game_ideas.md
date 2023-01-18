
Done 
----
One bird flapping around and bouncing off of screen edges
Multiple birds colliding with each other
  - Press keys to add and delete birds
Add new ball sprite, smaller than birds. Just rattling around and colliding.
  - balls can travel faster than birds (at start)
    - Note: collision algorithm meams birds that collide with balls will speed up and ball slows down (and vice versa)
  - Have different keys to start new birds and new balls
  - backspace deletes last object created


Python
------
Add walker at bottom of screen
  - Start game with "x" birds and 1 ball
  - if walker hit by bird, walker "catches" bird
    - bird disappears
    - new bird created
    - one more ball added
  - if walker hit by ball, ball rebounds and walker slows down -- making it harder to catch birds
Add score counter with timer and number of hits
  - When walker catches bird, score goes up
  - Timer resets when walker catches bird
  - Timer counts down and if timer reaches zero before walker catches next bird, then game over
   timer = score. Higher is better
As game goes along, the timer gets shorter

Change logic so game clock is multiplied
  - fastest object moves one pixel per clock
  - slowest object moves one pixel per "fastest-sprite-speed" clocks
  - hopefully solves collision issues?

More "Pyxel"-related tech:
--------------------------
Add background showing ground and sky
Add music and sound effects


   