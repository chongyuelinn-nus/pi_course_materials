import board
import busio
import time
import matplotlib.pyplot as plt
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1015(i2c)
chan = AnalogIn(ads, ADS.P0, ADS.P1)
 
t = ()
val = ()
for i in range(0,1000):
    t = t + (i,)
    val = val + (chan.voltage,)
plt.plot(t,val,'r--')
plt.show()
