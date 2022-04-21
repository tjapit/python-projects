# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:29:04 2021

@author: Peter
"""

import RPi.GPIO as GPIO   
from time import sleep 
from time import time
import pylab as py

# # UnboundLocalError, variables that become local as they are assigned
# global AoutLastFR, AoutLastFL, AoutLastBR, AoutLastBL
# global countsFR, countsFL, countsBR, countsBL
    
# Disable warnings
GPIO.setwarnings(False)

# frequency of PWM signal for all motors
freq = 100 # Hz

def setup_Motor_GPIOs(en, in1, in2): # function to setup motor GPIOs
    GPIO.setup(en,GPIO.OUT)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)


# constants
CPR = 7900.8
pi = 3.141592654
R = 4/100



# Encoder Functions ###########################################################
def getCounts(Aout,Bout,AoutLastState):
    AoutState = GPIO.input(Aout)
    BoutState = GPIO.input(Bout)
    if AoutState != AoutLastState:
        if BoutState != AoutState:
            dcounts = 1
        else:
            dcounts = -1
    else:
        dcounts = 0

    return dcounts, AoutState

# Functions to control a motor ################################################
def spin_forward(in1, in2):
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

def spin_backward(in1, in2):
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)

def set_speed(p,DC,v,vr):
    kp = .15*1250
    E = vr - v
    DC += kp*E
    DC = round(DC)
    if DC > 100:
        DC = 100
    elif DC < 0:
        DC = 0
    p.ChangeDutyCycle(DC)
    return DC

def stop(in1, in2):
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    

# Get Input Commands ##########################################################
def goDistancePrompts():
    """Prompts user to enter direction, speed, and distance of movement.

    Returns:
        str:direction forward/backwards
        float:distance of travel in meters
        float:speed of travel in centimeters per second
    """    
    print('Enter Direction')
    print('f - forward')
    print('b - backward')
    dir = input()
    while dir != 'f' and dir != 'b':
        print('Error: Invalid Direction')
        print('Enter Direction')
        print('f - forward')
        print('b - backward')
        dir = input()
        
    print('Enter distance to travel (in m)')
    xr = input()
    while(1):
        try: 
            xr = float(xr)
            break
        except:
            print('Error: Input Cannot Be Converted to Float')
            print('Enter Distance to travel (in m)')
            xr = input()

    print('Enter speed (in cm/s):')
    vr = input()
    while(1):
        try:
            vr = float(vr)/100
            break
        except:
            print('Error: Input Cannot Be Converted to Float')
            print('Enter speed (in cm/s)')
            vr = input()
    return dir, xr, vr

def goDistance(dir, xr, vr):
    """Moves the rover with the specified direction, distance, and speed.
    
    Args:
        dir (String):specified direction to move (forward/backward)
        xr (float):specified distance to move in meters
        vr (float):specified speed to move in meters per second
    
    Returns:
        float:actual distance traveled
    """
#     #debug
#     print(f"{dir} {vr} {xr}")
    # Motor setup #################################################################
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    # FR motor
    enFR = 18
    in1FR = 1
    in2FR = 6
    setup_Motor_GPIOs(enFR, in1FR, in2FR)
    pFR = GPIO.PWM(enFR,freq)
    pFR.start(0) 

    # FL motor
    enFL = 12
    in1FL = 17
    in2FL = 27
    setup_Motor_GPIOs(enFL, in1FL, in2FL)
    pFL = GPIO.PWM(enFL,freq)
    pFL.start(0) 

    # BR motor
    enBR = 13
    in1BR = 14
    in2BR = 15
    setup_Motor_GPIOs(enBR, in1BR, in2BR)
    pBR = GPIO.PWM(enBR,freq)
    pBR.start(0) 

    # BL motor
    enBL = 19
    in1BL = 23
    in2BL = 24
    setup_Motor_GPIOs(enBL, in1BL, in2BL)
    pBL = GPIO.PWM(enBL,freq)
    pBL.start(0) 

    # Encoder Setup ###############################################################
    # Front Right
    AoutFR = 10
    BoutFR = 9
    GPIO.setup(AoutFR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BoutFR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    countsFR = 0
    AoutLastFR = GPIO.input(AoutFR)

    # Front Left
    AoutFL = 26
    BoutFL = 22
    GPIO.setup(AoutFL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BoutFL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    countsFL = 0
    AoutLastFL = GPIO.input(AoutFL)

    # Back Right
    AoutBR = 11
    BoutBR = 7
    GPIO.setup(AoutBR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BoutBR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    countsBR = 0
    AoutLastBR = GPIO.input(AoutBR)

    # Back Left
    AoutBL = 25
    BoutBL = 8
    GPIO.setup(AoutBL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BoutBL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    countsBL = 0
    AoutLastBL = GPIO.input(AoutBL)
    ########################################################
    x = 0
    # initialize postion and speed
    xFR = 0; vFR = 0
    xFL = 0; vFL = 0
    xBR = 0; vBR = 0 
    xBL = 0; vBL = 0

    # reference speed
    vr = 4/100 # m/s
    # guess for current DC
    DC = 0 

    DCFR = set_speed(pFR,DC,vFR,vr)
    DCFL = set_speed(pFL,DC,vFL,vr)
    DCBR = set_speed(pBR,DC,vBL,vr)
    DCBL = set_speed(pBL,DC,vBR,vr)

    if dir == 'f':
        spin_forward(in1FR,in2FR)
        spin_forward(in1FL,in2FL)
        spin_forward(in1BR,in2BR)
        spin_forward(in1BL,in2BL)
        
    elif dir == 'b':
        spin_backward(in1FR,in2FR)
        spin_backward(in1FL,in2FL)
        spin_backward(in1BR,in2BR)
        spin_backward(in1BL,in2BL)
        x = -x
     
    # time step
    dtr = 0.01
    t0 = time()
    T0 = t0
    
    # Loop ########################################################################
    while x < xr:
        
        dcounts, AoutLastFR = getCounts(AoutFR,BoutFR,AoutLastFR)
        countsFR += dcounts
        dcounts, AoutLastFL = getCounts(AoutFL,BoutFL,AoutLastFL)
        countsFL -= dcounts
        dcounts, AoutLastBR = getCounts(AoutBR,BoutBR,AoutLastBR)
        countsBR += dcounts
        dcounts, AoutLastBL = getCounts(AoutBL,BoutBL,AoutLastBL) 
        countsBL -= dcounts
        
        dt = time() - t0
        if dt > dtr:
            # FR wheel
            dxFR = 2*pi*R*2*countsFR/CPR
            xFR += dxFR
            vFR = dxFR/dt            
            # FL wheel
            dxFL = 2*pi*R*2*countsFL/CPR
            xFL += dxFL
            vFL = dxFL/dt                
            # BR wheel
            dxBR = 2*pi*R*2*countsBR/CPR
            xBR += dxBR
            vBR = dxBR/dt                
            # BL wheel
            dxBL = 2*pi*R*2*countsBL/CPR
            xBL += dxBL
            vBL = dxBL/dt
            
            # adjust speed as necessary
            DCFR = set_speed(pFR,DCFR,vFR,vr)
            DCFL = set_speed(pFL,DCFL,vFL,vr)
            DCBR = set_speed(pBR,DCBR,vBR,vr)
            DCBL = set_speed(pBL,DCBL,vBL,vr)
            
            # update position
            x = (xFR + xFL + xBR + xBL)/4
            v = (vFR + vFL + vBR + vBL)/4
            #print('Distance: %8.3f m     Speed: %8.2f cm/s' % (x, 100*v))
            #print('vFR: %6.2f cm/s vFL: %6.2f cm/s vBR: %6.2f cm/s vBL: %6.2f cm/s' % (100*vFR, 100*vFL, 100*vBR, 100*vBL))
            print('xFR: %6.2f m xFL: %6.2f m xBR: %6.2f m xBL: %6.2f m' % (xFR, xFL, xBR, xBL))
            # Reset time and counts
            t0 = time()
            countsFR = 0
            countsFL = 0
            countsBR = 0
            countsBL = 0
            
            """debug: encoder works once plots are commented out
            # plot speed
            l1 = py.plot(time()-T0,100*vFR,'.b')
            l2 = py.plot(time()-T0,100*vFL,'.r')
            l3 = py.plot(time()-T0,100*vBR,'.g')
            l4 = py.plot(time()-T0,100*vBL,'.c')
            """
            
        
        
    # Stop all motors
    stop(in1FR,in2FR)
    stop(in1FL,in2FL)
    stop(in1BR,in2BR)
    stop(in1BL,in2BL)

    """debug: encoder works once plots are commented out
    # show the plot
    py.xlabel('t (s)')
    py.ylabel('v (cm/s)')
    #py.legend((l1,l2,l3,l4),('FR','FL','BR','BL'))
    py.show()
    """

    print('RTDT has travelled ' + str(x) + ' m')
    GPIO.cleanup()
    
    # return actual distance traveled
    return x

if __name__ == '__main__':
    dir, xr, vr = goDistancePrompts()
    goDistance(dir, xr, vr)
    
    
    
    
    
    

