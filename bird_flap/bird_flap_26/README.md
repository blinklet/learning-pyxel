# Version 26


Fix jitter solution
I think issue is due to floats. will try decimals in next version

Tried addiong partial distances when jitter is detected so that eventaully the x and y are in sync

but seemed to cause more sprites sticking to each other

Should go back to rounding solution
but how to solve the cycle of bad jitter detections?

(solved) the sprite to max sprite speed ratio is now a Fraction object. This allows precis ratios that will add up to whole numbers when expected
     reduces but does not eliminate jitter


(maybe remove jitter logic until future and focu on other game mechanics)
(done) removed complex jitter logic

(done) added snap method that rounds down sprite to a whole pixel value for x and y 
       call snap method when collision or wall detected



