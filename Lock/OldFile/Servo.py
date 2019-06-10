import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
pwm = GPIO.PWM(12,50)

pwm.start(0)
def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)
    
angle = 11
SetAngle(angle)
pwm.stop()
GPIO.cleanup()