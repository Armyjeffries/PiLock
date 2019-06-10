import RPi.GPIO as gpio
import MFRC522
import sys
import time
import signal
import shelve

continue_reading = True

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

unlock = 13
lock = 11


gpio.setup(unlock, gpio.OUT)
gpio.setup(lock, gpio.OUT)

lockStatus = 0

def doorStart():
    print "Locking the door to start:"
    gpio.output(lock, True)
    time.sleep(2.0)
    gpio.output(lock, False)
    global lockStatus
    lockStatus = 0
    

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

            idnumber = uid[0], uid[1], uid[2], uid[3]
            
            #print idnumber
            db = shelve.open('cardid')
            idnumberdb = db['Card UID']

            if idnumber == idnumberdb:            
                if  lockStatus == 0:
                    gpio.output(unlock, True)
                    time.sleep(2.0)
                    gpio.output(unlock, False)
                    global lockStatus
                    lockStatus = 1
                    print "Door Unlocked"
                else:
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
        MIFAREReader.MFRC522_StopCrypto1()
doorStart()
checkCard()   
