import board
import busio
import adafruit_mcp4725
import time

# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725.
dac = adafruit_mcp4725.MCP4725(i2c)

# ramp wave
# Main loop will go up and down through the range of DAC values forever.
while True:
    start = time.time()
    # Go up the 12-bit raw range.
    print('Going up 0-3.3V...')
    for i in range(4095):
        dac.raw_value = i
    # Go back down the 12-bit raw range.
    print('Going down 3.3-0V...')
    for i in range(4095, -1, -1):
        dac.raw_value = i
    end = time.time()
    print(end - start)
