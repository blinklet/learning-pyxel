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

(done) Change hit box on sprites to circles?

(done) cleaned up logic. Moved more update logic to sprite classes


