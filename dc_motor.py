import RPi.GPIO as GPIO
import time

HIGH = 1
LOW = 0

GPIO.setmode(GPIO.BCM)
dc_pwm_pin = 21
INT1_PIN = 20
INT2_PIN = 16

GPIO.setup(dc_pwm_pin, GPIO.OUT)
GPIO.setup(INT1_PIN, GPIO.OUT)
GPIO.setup(INT2_PIN, GPIO.OUT)

p = GPIO.PWM(dc_pwm_pin, 490)
p.start(5)


try:
    while True:
        print("Going CCW...")
        GPIO.output(INT1_PIN, HIGH)
        GPIO.output(INT2_PIN, LOW)
        p.ChangeDutyCycle(10)
        time.sleep(5)
        print("Going CCW, now faster...")
        p.ChangeDutyCycle(20)
        time.sleep(5)
        print("Going CW slowly...")
        GPIO.output(INT1_PIN, LOW)
        GPIO.output(INT2_PIN, HIGH)
        p.ChangeDutyCycle(10)
        time.sleep(5)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()

