# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 22:15:24 2021

@author: Peter
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:29:04 2021

@author: Peter
"""

import RPi.GPIO as GPIO   
from time import sleep  
import numpy as np

# Disable GPIO warnings
GPIO.setwarnings(False)

# Motor setup #################################################################
# frequency of PWM signal for all motors
freq = 100 # Hz

# # global variables
# global pFR, pFL, pBL, pBR

def setup_Motor_GPIOs(en, in1, in2): # function to setup motor GPIOs
    GPIO.setup(en,GPIO.OUT)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    


# MPU6050 Setup ###############################################################
import smbus            #import SMBus module of I2C          #import

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")

#defining roll, pitch, yaw
pitch = 0
roll = 0
yaw = 0

angle = 0

gyro_x0 = read_raw_data(GYRO_XOUT_H)
gyro_y0 = read_raw_data(GYRO_YOUT_H)
gyro_z0 = read_raw_data(GYRO_ZOUT_H)

# Functions to control a motor ################################################
def spin_forward(in1, in2):
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

def spin_backward(in1, in2):
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)

def set_speed(p,speed):
    p.ChangeDutyCycle(speed)

def stop(in1, in2):
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    

# Get Input Commands ##########################################################
def rotateAnglePrompts():
    """Prompts user to enter direction and angle of rotation.

    Returns:
        str:direction (l)eft/(r)ight
        float:distance of travel in meters
    """   
    # direction prompt
    print('Enter Direction')
    print('r - right')
    print('l - left')
    dir = input()
    
    # error checking for direction
    while dir != 'r' and dir != 'l':
        print('Error: Invalid Direction')
        print('Enter Direction')
        print('r - right')
        print('l - left')
        dir = input()
    
    # prompt for angle
    print('Enter Angle to Rotate to (in degrees)')
    angle_target = input()
    # error checking for angle
    while(1):
        try: 
            angle_target = float(angle_target)
            break
        except:
            print('Error: Input Cannot Be Converted to Float')
            print('Enter Angle to Rotate to (in degrees)')
            angle_target = input()
    # return direction and angle
    return dir, angle_target

def rotateAngle(dir, angle_target):
    """Rotates the rover to the specified direction and given angle.
    
    Args:
        dir (str):specified direction to rotate (right/left)
        angle_target (float):specified angle target to rotate to
    
    Returns:
        float:actual angle rotated
    """
    # debug: second time rotate fails because done only once through import
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
    angle = 0
    duty_cycle = 75

    set_speed(pFR,duty_cycle)
    set_speed(pFL,duty_cycle)
    set_speed(pBR,duty_cycle)
    set_speed(pBL,duty_cycle)

    if dir == 'r':
        spin_backward(in1FR,in2FR)
        spin_forward(in1FL,in2FL)
        spin_backward(in1BR,in2BR)
        spin_forward(in1BL,in2BL)
        angle_target = -angle_target
        
    elif dir == 'l':
        spin_forward(in1FR,in2FR)
        spin_backward(in1FL,in2FL)
        spin_forward(in1BR,in2BR)
        spin_backward(in1BL,in2BL)

     
    # time step
    dt = 0.01
    while abs(angle - angle_target) > 0.1:
       gyro_y = read_raw_data(GYRO_XOUT_H) - gyro_y0
       Gy = gyro_y/13.10
       angle += Gy*dt
       print(str(angle))
       sleep(dt)
        
    stop(in1FR,in2FR)
    stop(in1FL,in2FL)
    stop(in1BR,in2BR)
    stop(in1BL,in2BL)

    if dir == 'r':
        print('RTDT has rotated ' + str(-angle) + ' degrees right')
        
    elif dir == 'l':
        print('RTDT has rotated ' + str(angle) + ' degrees left')
    
    GPIO.cleanup()
    
    # return actual angle rotated
    return angle

if __name__ == '__main__':
    dir, angle_target = rotateAnglePrompts()
    rotateAngle(dir, angle_target)


    
    
    
    
    
    
    
