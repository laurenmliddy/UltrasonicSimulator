#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance via UltrasonicRanging sensor
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time
import statistics


trigPin = 16
echoPin = 18
MAX_DISTANCE = 220          # define the maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance

def pulseIn(pin,level,timeOut): # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def getSonar():     # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      # make trigPin output 10us HIGH level
    time.sleep(0.00001)     # 10us
    GPIO.output(trigPin,GPIO.LOW) # make trigPin output LOW level
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   # read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # calculate distance with sound speed 340m/s
    return distance

def setup():
    GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
    GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN) # set echoPin to INPUT mode

def getSample():
    sample=[]
    for i in range(60):
        distance = getSonar()
        sample.append(distance)
        time.sleep(0.05)
    return sample

def Hold():
    list = []
    list.append(getSonar())
    average = sum(list) / len(list)
    if (0.1*average):
        if average < 12:
            return 'Low Hold'
        elif average > 26 and average < 32:
            return 'High Hold'
    return 'Unknown'

def Pass():
    low = 6 <= getSonar() <= 12
    high = 26 <= getSonar() <= 32
    if low == True:
        return "Low Pass"
    if high == True:
        return "High pass"
    return 'Unknown'



#def PullUp(sample):
    #for i in range (1,len(sample)):
        #if (sample[i-1]>sample[i]):
            #return 'Unknown'
    #return 'Pull Up'


#def PushDown(sample):
    #for i in range(1, len(sample)):
        #if (sample[i-1]<sample[i]):
            #return 'Unknown'
    #return 'Push Down'

def PullUp():
    list = []
    list.append(getSonar())
    count = 0
    minimum = 3
    for i in range(len(list))[1:]:
        if list[i] > list[i-1] and abs(list[i]-list[i-1]) > minimum:
            count += 1
            return 'Pull Up'
        return 'Unknown'

def PushDown():
    list = []
    list.append(getSonar())
    count = 0
    minimum = 3
    for i in range(len(list))[1:]:
        if list[i] < list[i-1] and abs(list[i]-list[i-1]) > minimum:
            count += 1
            return 'Push Down'
        return 'Unknown'


def Movements():
    val = Hold()
    if val != 'Unknown':
        return val
    val = Pass()
    if val != 'Unknown':
        return val
    val = PullUp()
    if val != 'Unknown':
        return val
    val = PushDown()
    if val != 'Unknown':
        return val
    return 'Unknown'

def sequences():

    sequence = {
    'Start' : 'Low Pass',
    'Resume' : 'High Pass',
    'Stop' : 'Low Hold',
    'Pause' : 'High Hold',
    'Louder' : 'Pull Up',
    'Quieter' : 'Push Down',
    'Skip Forward' : ('Low Pass','Low Pass'),
    'Skip backward' : ('High Pass','High Pass'),
    'Power off' : ('Low Pass', 'Low Hold'),
    'Reset' : ('High Pass', 'High Hold'),
    'ActivateAutoMode' : ('Pull Up',('High Pass', 'Low Hold')),
    'DisableAutoMode' : ('Push Down',('Low Pass','High Hold'))
    }
    commard = sequence.get(Movements())
    print(commard)

def loop():
    ceiling = 100
    floor = 4
    flag = False
    while(True):
        distance = getSonar() # get distance
        if distance > ceiling or distance < floor:
            if not flag:
                list = []
            flag = True
            list.append(distance)
        elif distance >= ceiling:
            if flag:
                print(recognise(list))
            flag = False
        else:
            print ("The distance is : %.2f cm"%(distance))
            print(Movements())
            print(sequences())
            time.sleep(0.1)


if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        GPIO.cleanup()         # release GPIO resource