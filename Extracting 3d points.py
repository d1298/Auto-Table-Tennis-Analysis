#import cv2 to capture and deal with the video, mediapipe is used for the pose landmark detection
import cv2
import mediapipe as mp

#This function goes through the created landmarks for each frame, prints out the x,y, and z coordinates for each landmark, and records all of them to csv_data
def record_landmarks(landmarks, frame_number, csv_data):
    print("Landmark coordinates for frame " + str(frame_number))
    string = ""
    for idx, landmark in enumerate(landmarks):
        if idx in specific_landmarks_indices:
            print(mp_pose.PoseLandmark(idx).name + ": x=" + str(landmark.x) + ", y=" + str(landmark.y) + ", z=" + str(landmark.z))
            string += (str(landmark.x) + "," + str(landmark.y) + "," + str(landmark.z) + ",")

    csv_data.append(str(frame_number) + "," + string + "\n")
    print("\n")

#This makes it clearer to call the mp.solutions.pose and mp.solutions.drawing_utils which are used for detection and overlaying the points respectively
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

#This is a list of the landmarks that will be recorded
#Left shoulder, right shoulder, left elbow, right elbow, left wrist, right wrist, left hip, right hip, left knee, right knee, left ankle, right ankle
specific_landmarks_indices = [
    mp_pose.PoseLandmark.LEFT_SHOULDER.value,
    mp_pose.PoseLandmark.RIGHT_SHOULDER.value,
    mp_pose.PoseLandmark.LEFT_ELBOW.value,
    mp_pose.PoseLandmark.RIGHT_ELBOW.value,
    mp_pose.PoseLandmark.LEFT_WRIST.value,
    mp_pose.PoseLandmark.RIGHT_WRIST.value,
    mp_pose.PoseLandmark.LEFT_HIP.value,
    mp_pose.PoseLandmark.RIGHT_HIP.value,
    mp_pose.PoseLandmark.LEFT_KNEE.value,
    mp_pose.PoseLandmark.RIGHT_KNEE.value,
    mp_pose.PoseLandmark.LEFT_ANKLE.value,
    mp_pose.PoseLandmark.RIGHT_ANKLE.value
]

#Start capturing video at either a file address (for an mp4) or a webcam input
cap = cv2.VideoCapture("video.mp4")

#error message
if not cap.isOpened():
    print("Error: Cannot access the camera.")
    exit()

frame_number = 0
#Array for the list to be saved, first line is the column headers   
csv_data = ["frame number, LSx, LSy,LSz,RSx,RSy,RSz,LEx,LEy,LEz,REx,REy,REz,LWx,LWy,LWz,RWx,RWy,RWz,LHx,LHy,LHz,RHx,RHy,RHz,LKx,LKy,LKz,RKx,RKy,RKz,LAx,LAy,LAz,RAx,RAy,RAz \n"]

#loop through the video
while cap.isOpened():
    #read the video, read is a boolean for whether or not the video is read, and frame is the frames image data
    read, frame = cap.read()
    
    #Error handling
    if not read:
        print("Failed to grab a frame. Exiting...")
        break

    #Use mediapipe to get the locations of each point in the frame
    result = pose.process(frame)

    #Draw circles on the image using cv2 to show the detected landmarks
    if result.pose_landmarks:
        for index in specific_landmarks_indices:
            landmark = result.pose_landmarks.landmark[index]
            height, width, _ = frame.shape
            cx, cy = int(landmark.x * width), int(landmark.y * height)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
        record_landmarks(result.pose_landmarks.landmark, frame_number, csv_data)

    #Show each frame, with the overlay
    cv2.imshow("Pose Detection", frame)

    #If q is pressed then exit the pgroam
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    #iterate through the frames of the video
    frame_number += 1

#Cleanly exit the program
cap.release()
cv2.destroyAllWindows()

#Record all of the data to the csv file for analysis
with open('recorded_data/test1.csv', 'w') as file:
    file.writelines(csv_data)