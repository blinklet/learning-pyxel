# Version 22


Fix jitter in sprite movement
issue is sawtooth pattern of diagonal movement due to rounding
Try to arrange so that pairs of values for slower objects match each other
for example, when fastest object is speed=2, an object with speed=1 should:
           (13.0,51.0)(13.5,50.5)(14.0,50.0)(14.5,49.5)
instead of (13,  51  )(14,  51  )(14,  50  )(15,  50  )
need       (13,  51  )(13,  51  )(14,  50  )(14,  50  )

int(abs(13.0)) - abs(13.5) = 0.5
int(abs(13.5)) - abs(14.0) = 1.0
int(abs(14.0)) - abs(14.5) = 0.5
int(abs(14.5)) - abs(15.0) = 1.0

int(abs(13.0)) - abs(13.33) = 0.33
int(abs(13.33)) - abs(13.67) = 0.67
int(abs(13.67)) - abs(14.0) = 1.0
int(abs(14.0)) - abs(14.33) = 0.33
int(abs(14.33)) - abs(14.67) = 0.67
int(abs(14.67)) - abs(15.0) = 1.0

abs(13.0)) - int(abs(13.5)) = 0
abs(13.5)) - int(abs(14.0)) = 0.5
abs(14.0)) - int(abs(14.5)) = 0
abs(14.5)) - int(abs(15.0)) = 0.5

abs(13.0) - int(abs(13.33)) = 0
abs(13.33) - int(abs(13.67)) = 0.33
abs(13.67) - int(abs(14.0)) = 0.67
abs(14.0) - int(abs(14.33)) = 0
abs(14.33) - int(abs(14.67)) = 0.33
abs(14.67) - int(abs(15.0)) = 0.67
