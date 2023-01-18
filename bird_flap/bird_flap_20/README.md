# Version 20

Split the program into separate modules to make it more manageable
- game.py  (the main app)
- Sprite  (defines the Sprite class)
- GameSprites  (defines subclasses of the Sprite class)


Changed logic so game clock is multiplied
  - fastest object moves one pixel per clock
  - slowest object moves one pixel per "fastest-sprite-speed" clocks
  - hopefully solves collision issues?

Also got biggest sprite sizes to help with screen size and max sprites calculations

Also cleaned up the modules so I do not import Sprite class into game.py
I import game_sprites, which is the only module that imports sprites, now
