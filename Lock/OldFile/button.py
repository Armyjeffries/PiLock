import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.OUT)

while True:
    if GPIO.input(37) == GPIO.HIGH:
        print("Button was pushed!")
        time.sleep(.5)
        GPIO.output(17, False)
        time.sleep(1)
        print ("relay on!")
        