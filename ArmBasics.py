
#David Meyer
#Running the motor check

import time
import sys

from adafruit_motorkit import MotorKit


def clawOp():
    print("Claw Open ")
    kit.motor4.throttle = -.2
    time.sleep(0.25)
    kit.motor4.throttle = 0 #stop
    time.sleep(0.5)
#end
    
def clawClose():
    print("Claw Open ")
    kit.motor4.throttle = -.5
    time.sleep(0.25)
    kit.motor4.throttle = 0 #stop
    time.sleep(0.5)
#end

def armOne(num, t):
    print("Arm 1 Up")
    kit.motor1.throttle = num
    time.sleep(t)
    kit.motor1.throttle = 0
    time.sleep(0.5)
#end

def armTwo(num, t):
    print("Arm 2 Down")
    kit.motor3.throttle = num
    time.sleep(t)
    kit.motor3.throttle = 0
    time.sleep(0.5)
#end
def twist(num, t):
    print("TwistR")
    kit.motor2.throttle = num
    time.sleep(t)
    kit.motor2.throttle = 0
    time.sleep(0.5)
#end
def test1():
    twist(0.3)
    claw(.5)  #close
    claw(-.5) #open
    
def checkMate():
    clawClose()
    clawOp()
    clawClose()
    clawOp()
    
def a11():
    twist(.4, .3)
    armOne(.6, .4)
    armTwo(-.95, .35)
    
    #clawClose()
    
    #armOne(-.6, .4)  #Good up to here!!!
    #armTwo(.3,.3)
    #twist(-0.4, .3)
def a12():
    twist(.335, .3)
    
def a13():
    twist(.258, .3)

def a14():
    twist(.165, .4)

kit = MotorKit()

print("start motor")

a11()
#clawOp()

sys.exit()
