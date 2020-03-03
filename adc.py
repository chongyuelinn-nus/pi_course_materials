import board
import busio
import time
print ("starting up... this may take awhile...")
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1015(i2c, gain=2/3)
chan = AnalogIn(ads, ADS.P0, ADS.P1)
 
t = ()
val = ()
for i in range(0,1000):
    t = t + (i,)
    print(chan.voltage)
    time.sleep(0.3)
