import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(5) # Initialization
pause_t = 1
try:
    while True:
        p.ChangeDutyCycle(7.5)
        time.sleep(pause_t)
        p.ChangeDutyCycle(10)
        time.sleep(pause_t)
        p.ChangeDutyCycle(5)
        time.sleep(pause_t)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
