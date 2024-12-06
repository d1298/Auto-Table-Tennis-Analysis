import cv2 
import time
import keyboard
import math
import numpy as np
from sympy import *
from sympy.abc import *

x,y = symbols("x y ")

cap = cv2.VideoCapture("video.mp4")

if not cap.isOpened():
    print("Error: Cannot access the camera.")
    exit()
    
shots = ["BPush", "BBlock", "BDrive", "FPush", "FBlock", "FDrive"]

frame_number = 0
bp,bb,bd,fp,fb,fd = False, False, False, False, False, False

#The idea to train a model with video data.
#Calculate the angles between all of the joins that we want
# Work out an equation for each of the angles throughout the process of the shot
# This will be the training data

#Where B is the centre angle, aka angle(ABC)
def get_angle(ax,ay,az,bx,by,bz,cx,cy,cz):
    AB = math.sqrt((ax-bx)**2 + (ay-by)**2 + (az-bz)**2)
    BC = math.sqrt((bx-cx)**2 + (by-cy)**2 + (bz-cz)**2)
    AC = math.sqrt((ax-cx)**2 + (ay-cy)**2 + (az-cz)**2)
    
    #cosine rule 
    angle = math.degrees(math.acos((AB**2 + BC**2 - AC**2) / (2*AB*BC)))
    return angle

def write_data(data):
    with open("recorded_data/detecting_shots.csv", "a") as file:
        file.writelines(data)
        
        
def lagrange_interpolation(y_values):
    n = len(y_values)
    x_values = list(range(n))
    
    
    equation = 0
    print(y_values, x_values)
    
    for yval in range(n):
        numerator = 1
        denominator = 1
        
        for xval in range(n):
            if xval != yval:
                numerator *= (x - x_values[xval])
                denominator *= (x_values[yval] - x_values[xval])
            
        equation += (numerator/denominator) * y_values[yval]
        
    equation = expand(equation)
        
    return equation

def frames_to_equations(shot-index,starting_frame, ending_frame):
    with open ("recorded_data/test1.csv", "r") as file:
        datatemp = file.read().splitlines()
        data = []
        for i in range(1,len(datatemp)):
            data.append(datatemp[i].split(","))
            
        angles = []
            
        for i in range(ending_frame - starting_frame):
            angles.append([])
            frame_index = starting_frame + i

            opts = [[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],[16,17,18],[19,20,21],[22,23,24],[25,26,27],[28,29,30],[31,32,33],[34,35,36]]
            for a in range(12):
                for b in range(12):
                    for c in range(12):
                        angles[i].append(get_angle(data[frame_index][opts[a][0]],data[frame_index][opts[a][1]],data[frame_index][opts[a][2]],data[frame_index][opts[b][0]],data[frame_index][opts[b][1]],data[frame_index][opts[b][2]],data[frame_index][opts[c][0]],data[frame_index][opts[c][1]],data[frame_index][opts[c][2]]))
            
        equations = [starting_frame, ending_frame]
                    
        for i in range(len(angles[0])):
            anglestoequation = []
            for b in range(len(angles)):
                anglestoequation.append(angles[b][i])
            equations.append(lagrange_interpolation(anglestoequation))
        write_data(equations)
        print("written data")



#Probably use polynomial interpolation (newton) to approximate the equation, offset all frame numbers so the first one is zero to simplify the whole thing

#0,1,2,3,4,5,6
#BPush, BBlock, BDrive, FPush, FBlock, FDrive

#frame number, LSx,LSy,LSz,  RSx,RSy,RSz,  LEx,LEy,LEz,  REx,REy,REz,  LWx,LWy,LWz,  RWx,RWy,RWz,  LHx,LHy,LHz,  RHx,RHy,RHz,  LKx,LKy,LKz,  RKx,RKy,RKz,  LAx,LAy,LAz,  RAx,RAy,RAz
#   0            1  2   3     4   5   6     7   8   9     10  11  12   13  14  15    16  17  18     19  20  21    22  23  24    25  26  27    28  29  30    31  32  33    34  35  36



while cap.isOpened():
    read, frame = cap.read()
    
    if not read:
        print("Failed to grab a frame. Exiting...")
        break
    
    cv2.imshow("Video", frame)
    
    #need to simplify this --------------------------
    if keyboard.is_pressed("1"): 
        if bp == False:
            print("Backhand Push Started", frame_number)
            starting_frame = frame_number
            bp = True
        elif bp == True:
            print("Backhand Push Ended",frame_number)
            ending_frame = frame_number
            frames_to_equations(0,starting_frame,ending_frame)
            bp = False
    
    if keyboard.is_pressed("2"): 
        if bb == False:
            print("Backhand Block Started", frame_number)
            starting_frame = frame_number
            bb = True
        if bb == True:
            print("Backhand Block Ended",frame_number)
            ending_frame = frame_number
            frames_to_equations(1,starting_frame,ending_frame)
            bb = False        
            
    if keyboard.is_pressed("3"): 
        if bd == False:
            print("Backhand Drive Started", frame_number)
            starting_frame = frame_number
            bd = True
        if bd == True:
            print("Backhand Drive Ended",frame_number)
            ending_frame = frame_number
            frames_to_equations(2,starting_frame,ending_frame)
            bd = False
    
    if keyboard.is_pressed("4"): 
        if fp == False:
            print("Forehand Push Started", frame_number)
            starting_frame = frame_number
            fp = True
        if fp == True:
            print("Forehand Push Ended",frame_number)
            ending_frame = frame_number
            frames_to_equations(3,starting_frame,ending_frame)
            fp = False
                
    if keyboard.is_pressed("5"): 
        if fb == False:
            print("Forehand Block Started", frame_number)
            starting_frame = frame_number
            fb = True
        if fb == True:
            print("Forehand Block Ended",frame_number)
            ending_frame = frame_number
            frames_to_equations(4,starting_frame,ending_frame)
            fb = False       
                
    if keyboard.is_pressed("6"): 
        if fd == False:
            print("Forehand Drive Started", frame_number)
            starting_frame = frame_number
            fd = True
        if fd == True:
            print("Forehand Drive Ended",frame_number)
            ending_frame = frame_number
            frames_to_equations(5,starting_frame,ending_frame)
            fd = False               
    # ------------------------------------------------------------------------------
    
    
        
            
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    frame_number += 1
    
    time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()

