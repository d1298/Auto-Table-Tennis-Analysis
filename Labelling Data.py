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

while cap.isOpened():
    read, frame = cap.read()
    
    if not read:
        print("Failed to grab a frame. Exiting...")
        break
    
    cv2.imshow("Video", frame)
    
    if keyboard.is_pressed("1"): 
        if bp == True:
            print("Backhand Push",frame_number)
    
    if keyboard.is_pressed("2"): 
        print("Backhand Block",frame_number)
        
    if keyboard.is_pressed("3"): 
        print("Backhand Drive",frame_number)
    
    if keyboard.is_pressed("4"): 
        print("Forehand Push",frame_number)
    
    if keyboard.is_pressed("5"): 
        print("Forehand Block",frame_number)
        
    if keyboard.is_pressed("6"): 
        print("Forehand Drive",frame_number)
        
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    frame_number += 1
    
    time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()

