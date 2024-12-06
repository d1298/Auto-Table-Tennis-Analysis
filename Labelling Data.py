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
    ax,ay,az,bx,by,bz,cx,cy,cz = float(ax), float(ay), float(az), float(bx), float(by), float(bz), float(cx), float(cy), float(cz)
    
    
    AB = math.sqrt((ax-bx)**2 + (ay-by)**2 + (az-bz)**2)
    BC = math.sqrt((bx-cx)**2 + (by-cy)**2 + (bz-cz)**2)
    AC = math.sqrt((ax-cx)**2 + (ay-cy)**2 + (az-cz)**2)
        
    #cosine rule 
    angle = math.degrees(math.acos(float(AB**2 + BC**2 - AC**2) / float(2.0*AB*BC)))
    return angle

def write_data(data):
    with open("recorded_data/detecting_shots.csv", "w") as file:
        file.writelines(str(data))
        print("written data")
        return
        
        
def lagrange_interpolation(y_values):
    n = len(y_values)
    x_values = list(range(n))
    
    equation = 0
    
    for yval in range(n):
        numerator = 1
        denominator = 1
        
        for xval in range(n):
            if xval != yval:
                numerator *= (x - x_values[xval])
                denominator *= (x_values[yval] - x_values[xval])
            
        equation += (numerator/denominator) * y_values[yval]
        
    equation = expand(equation)
    print(equation)
        
    return equation

def frames_to_equations(shot,starting_frame, ending_frame):
    
    shots = {
        0: "None",
        1: "Backhand Push",
        2: "Backhand Block",
        3: "Backhand Drive",
        4: "Forehand Push",
        5: "Forehand Block",
        6: "Forehand Drive"
    }
    
    print(shots[shot] + " ended")
    
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
                        if a != b and b != c and a != c:
                            angles[i].append(get_angle(data[frame_index][(opts[a])[0]],data[frame_index][(opts[a])[1]],data[frame_index][(opts[a])[2]],data[frame_index][(opts[b])[0]],data[frame_index][(opts[b])[1]],data[frame_index][(opts[b])[2]],data[frame_index][(opts[c])[0]],data[frame_index][(opts[c])[1]],data[frame_index][(opts[c])[2]]))
            
        equations = [shot,starting_frame, ending_frame]
                    
        for i in range(len(angles[0])):
            anglestoequation = []
            for b in range(len(angles)):
                anglestoequation.append(angles[b][i])
            equations.append(lagrange_interpolation(anglestoequation))
            
        write_data(equations)
        return

#Probably use polynomial interpolation (newton) to approximate the equation, offset all frame numbers so the first one is zero to simplify the whole thing

#0,1,2,3,4,5,6
#BPush, BBlock, BDrive, FPush, FBlock, FDrive

#frame number, LSx,LSy,LSz,  RSx,RSy,RSz,  LEx,LEy,LEz,  REx,REy,REz,  LWx,LWy,LWz,  RWx,RWy,RWz,  LHx,LHy,LHz,  RHx,RHy,RHz,  LKx,LKy,LKz,  RKx,RKy,RKz,  LAx,LAy,LAz,  RAx,RAy,RAz
#   0            1  2   3     4   5   6     7   8   9     10  11  12   13  14  15    16  17  18     19  20  21    22  23  24    25  26  27    28  29  30    31  32  33    34  35  36

def end_recording( shot, frame_number, starting_frame):
    
    frames_to_equations(shot,starting_frame,frame_number)
    time.sleep(0.1)

    return

while cap.isOpened():
    read, frame = cap.read()
    
    if not read:
        print("Failed to grab a frame. Exiting...")
        break
    
    cv2.imshow("Video", frame)
    
    if keyboard.is_pressed(" "): 
        starting_frame = frame_number
        time.sleep(0.1)
    
    elif keyboard.is_pressed("1"): 
        end_recording(1, frame_number, starting_frame)
    
    elif keyboard.is_pressed("2"): 
        end_recording(2, frame_number, starting_frame)
        
    elif keyboard.is_pressed("3"): 
        end_recording(3, frame_number, starting_frame)

    elif keyboard.is_pressed("4"): 
        end_recording(4, frame_number, starting_frame)
      
    elif keyboard.is_pressed("5"): 
        end_recording(5, frame_number, starting_frame)
    
    elif keyboard.is_pressed("6"): 
        end_recording(6, frame_number, starting_frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    frame_number += 1
    
    time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()

