#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicSimulator.py
# Description : Get gestures by simulating UltrasonicRanging sensor
# Author      : Panagiotis Alefragkis, LSBU
# modification: 2021/02/07
########################################################################
from secrets import randbelow
import time
import random

def getSonar():
    return random.uniform(0,200.0)

def getFakeCeiling():
    return 180 + random.uniform(0,3.0)

def getFakeHigh():
    return 40 + random.uniform(0,3.0)

def getFakeLow():
    return 9 + random.uniform(0,3.0)

def getRandomSample(N=20):
    sample = []
    delay = 1/N
    for i in range(N):
        distance = getSonar() # get distance
        sample.append(distance)
        time.sleep(delay)
    return sample

def getPass(value): 
    if(value < 24):
        return "Low Pass"
    if(25<= value <=55):
        return "High pass"
    return value

def getPasses():
    values = [];
    randomSample = getRandomSample() 
    for i in randomSample:
        value = getPass(i)
        values.append(value)

    return values

def PullUp():
    for i in range (1,getRandomSample(),1):
        if (getRandomSample()[i-1]>getRandomSample()[i]):
            return 'Unknown'
    return 'Pull Up'
    

def createFakePushDown(N=20):
    val = []
    delay = 1/N
    current = 40 + random.uniform(0,15.0)
    for i in range(N):
        val.append(current)
        current -= random.uniform(0,2.0)
        time.sleep(delay)
    return val

def createFakePushUp(N=20):
    val = []
    delay = 1/N
    current = 5 + random.uniform(0,10.0)
    for i in range(N):
        val.append(current)
        current += random.uniform(0,2.0)
        time.sleep(delay)
    return val

def createFakeHighHold(N=20):
    val = []
    delay = 1/N
    for i in range(N):
        val.append(getFakeHigh())
        time.sleep(delay)
    return val

def createFakeLowHold(N=20):
    val = []
    delay = 1/N
    for i in range(N):
        val.append(getFakeLow())
        time.sleep(delay)
    return val

def createFakeLowPass(N=20):
    val = []
    delay = 1/N
    low = 2+random.randrange(0.2*N)
    high  = int(0.8*N)+ random.randrange(0.2*N)
    for i in range(low):
        val.append(getFakeCeiling())
        time.sleep(delay)
    for i in range(low,high):
        val.append(getFakeLow())
        time.sleep(delay)
    for i in range(high,N):
        val.append(getFakeCeiling())
        time.sleep(delay)
    return val

def createFakeHighPass(N=20):
    val = []
    delay = 1/N
    low = 2+random.randrange(0.2*N)
    high  = int(0.8*N)+ random.randrange(0.2*N)
    for i in range(low):
        val.append(getFakeCeiling())
        time.sleep(delay)
    for i in range(low,high):
        val.append(getFakeHigh())
        time.sleep(delay)
    for i in range(high,N):
        val.append(getFakeCeiling())
        time.sleep(delay)
    return val


def createFakeMove(N=20):
    move = random.randrange(7.0)
    if move == 0:
        return createFakeLowHold(N)
    elif move == 1:
        return createFakeHighHold(N)
    elif move == 2:
        return createFakeHighPass(N)
    elif move == 3:
        return createFakeLowPass(N)
    elif move == 4:
        return createFakePushDown(N)
    elif move == 5:
        return createFakePushUp(N)
    elif move == 6:
        return getRandomSample(N)

def getSample(N=20):
    return createFakeMove(N)

def setup():
    print ('Simulator is starting...')

def cleanup():
    print ('Simulator is shuting down...')
    
def test():
    while(True):
        sample = getPasses()
        # print ("Sample:"+str(['{:.2f}'.format(x) for x in sample]))
        print(sample)
            
if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        test()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        cleanup()
        print ('Bye...')

