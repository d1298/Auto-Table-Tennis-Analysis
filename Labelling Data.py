import cv2 
import time
import keyboard

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

def get_angles(ax,ay,az,bx,by,bz,cx,cy,cz):
    pass


while cap.isOpened():
    read, frame = cap.read()
    
    if not read:
        print("Failed to grab a frame. Exiting...")
        break
    
    cv2.imshow("Video", frame)
    
    if keyboard.is_pressed("1"): 
        if bp == False:
            print("Backhand Push Started", frame_number)
            bp = True
        if bp == True:
            print("Backhand Push Ended",frame_number)
            bp = False
    
    if keyboard.is_pressed("2"): 
        if bb == False:
            print("Backhand Block Started", frame_number)
            bb = True
        if bb == True:
            print("Backhand Block Ended",frame_number)
            bb = False        
            
    if keyboard.is_pressed("3"): 
        if bd == False:
            print("Backhand Drive Started", frame_number)
            bd = True
        if bd == True:
            print("Backhand Drive Ended",frame_number)
            bd = False
    
    if keyboard.is_pressed("4"): 
        if fp == False:
            print("Forehand Push Started", frame_number)
            fp = True
        if fp == True:
            print("Forehand Push Ended",frame_number)
            fp = False
                
    if keyboard.is_pressed("5"): 
        if fb == False:
            print("Forehand Block Started", frame_number)
            fb = True
        if fb == True:
            print("Forehand Block Ended",frame_number)
            fb = False       
                 
    if keyboard.is_pressed("6"): 
        if fd == False:
            print("Forehand Drive Started", frame_number)
            fd = True
        if fd == True:
            print("Forehand Drive Ended",frame_number)
            fd = False               
            
            
            
        
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    frame_number += 1
    
    time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()

