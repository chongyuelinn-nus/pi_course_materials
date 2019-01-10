import board
import busio
import time
import matplotlib.pyplot as plt
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
ads = ADS.ADS1015(i2c, gain=1)
chan = AnalogIn(ads, ADS.P0, ADS.P1)
 
while True:
    dist = 27 / chan.voltage
    v = chan.voltage *1023.0/5.0
    if v < 10:
        dist = 10
    else:
        # http://www.limulo.net/website/coding/physical-computing/sharp-linearization.html
        dist = ((6787.0 / (v - 3.0)) - 4.0)
    print ("voltage: ", chan.voltage, "; dist in cm: ", dist)
    time.sleep(1)
