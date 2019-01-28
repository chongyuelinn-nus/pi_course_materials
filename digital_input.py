import RPi.GPIO as GPIO 
import time

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 21 

GPIO.setup(GPIO_TRIGGER, GPIO.IN) 

while True:
    print (GPIO.input(GPIO_TRIGGER))

GPIO.cleanup()
