import RPi.GPIO as GPIO 
import time

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 21 

GPIO.setup(GPIO_TRIGGER, GPIO.IN) 

#GPIO.output(GPIO_TRIGGER, False)
while True:
    print (GPIO.input(GPIO_TRIGGER))

#GPIO.output(GPIO_TRIGGER, True) 
#while True:
#	GPIO.output(GPIO_TRIGGER, True) 
#	time.sleep(1)
#	print("setting to high")

GPIO.cleanup()
