# move car forward turn left, turn right, then  reverse in a straight line

import time
import donkeycar
from donkeycar.parts.actuator import PCA9685

steering_channel = 0
throttle_channel = 1

steering_controller = PCA9685(steering_channel)
throttle_controller = PCA9685(throttle_channel)

throttle_controller.run(420)

steering_controller.run(510)
time.sleep(1)
steering_controller.run(250)
time.sleep(1)

steering_controller.run(380)
throttle_controller.run(400)
time.sleep(0.1)

# moving backwards
throttle_controller.run(350)
time.sleep(0.1)
throttle_controller.run(400)
time.sleep(0.1)
throttle_controller.run(360)
time.sleep(3)
throttle_controller.run(400)



