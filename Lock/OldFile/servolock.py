import RPi.GPIO as gpio
import MFRC522
import sys
import time
import signal
import pickle
import os

continue_reading = True

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

unlock = 13
lock = 11
servo = 12
button = 37

gpio.setwarnings(False)
gpio.setup(unlock, gpio.OUT)
gpio.setup(lock, gpio.OUT)
gpio.setup(servo, gpio.OUT)
gpio.setup(button, gpio.IN.pull_up_down=gpio.PUD_DOWN)
pwm = gpio.PWM(servo, 50)

pwm.start(0)

lockStatus = 0
angle = 25

IDlist = 'IDlist.dat'

with open(IDlist, 'rb') as rfp:
    IDs = pickle.load(rfp)
    
def SetAngle(angle):
    duty = angle / 18 + 2
    gpio.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    gpio.output(12, False)
    pwm.ChangeDutyCycle(0)

def doorStart():
    print "Locking the door to start:"
    gpio.output(lock, True)
    time.sleep(2.0)
    gpio.output(lock, False)
    global lockStatus
    lockStatus = 0
    SetAngle(angle)
    

def notAuth(status):
    gpio.output(lock, status)
    gpio.output(unlock, status)

def checkCard():
    while 1:
    
    # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"
    
    # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            idnumber = (uid[0], uid[1], uid[2], uid[3])
            
            #print idnumber
            if idnumber in IDs:            
                if  lockStatus == 0:
                    global angle
                    angle = 180
                    SetAngle(angle)
                    gpio.output(unlock, True)
                    time.sleep(2.0)
                    gpio.output(unlock, False)
                    global lockStatus
                    lockStatus = 1
                    
                    print "Door Unlocked"
                else:
                    global angle
                    angle = 25
                    SetAngle(angle)
                    gpio.output(lock, True)
                    time.sleep(2.0)
                    gpio.output(lock, False)
                    global lockStatus
                    lockStatus = 0
                    
                    print "Door Locked"
            else:
                print "Card not authorized"
                notAuth(True)
                time.sleep(0.2)
                notAuth(False)
                time.sleep(0.2)
                notAuth(True)
                time.sleep(0.2)
                notAuth(False)
                time.sleep(0.2)
                notAuth(True)
                time.sleep(0.2)
                notAuth(False)
                   
        # Stop
        if gpio.input(button) == gpio.HIGH:
            if  lockStatus == 0:
                    global angle
                    angle = 180
                    SetAngle(angle)
                    gpio.output(unlock, True)
                    time.sleep(2.0)
                    gpio.output(unlock, False)
                    global lockStatus
                    lockStatus = 1
                    
                    print "Door Unlocked"
                else:
                    global angle
                    angle = 25
                    SetAngle(angle)
                    gpio.output(lock, True)
                    time.sleep(2.0)
                    gpio.output(lock, False)
                    global lockStatus
                    lockStatus = 0
                    
                    print "Door Locked"
        MIFAREReader.MFRC522_StopCrypto1()
doorStart()
checkCard()   
