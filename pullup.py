import RPi.GPIO as GPIO 
import time

GPIO.setmode(GPIO.BCM)

OUTPUT_PIN = 21 

GPIO.setup(OUTPUT_PIN, GPIO.OUT) 

GPIO.output(OUTPUT_PIN, False)
sending = False
while True:
    if sending:
        GPIO.output(OUTPUT_PIN, False)
        print("setting to low")
        sending = False
    else:
        GPIO.output(OUTPUT_PIN, True)
        print("setting to high")
        sending = True
    time.sleep(0.5) 

GPIO.cleanup()
