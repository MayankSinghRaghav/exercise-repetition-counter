#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install mediapipe opencv-python matplotlib')


# In[ ]:


import cv2
import mediapipe as mp

# Initialize mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Load video
cap = cv2.VideoCapture("demo video.mp4")

counter = 0     
stage = None
sets = 0        
SET_SIZE = 10   

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Track left hip & knee for squat detection
        hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
        knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y

        # Squat counting rule
        if hip > knee and stage != "down":
            stage = "down"
        if hip < knee and stage == "down":
            stage = "up"
            counter += 1

            # Check if a set is completed
            if counter % SET_SIZE == 0:
                sets += 1
                print(f"🎯 Set {sets} completed!")

        # Overlay reps and sets
        cv2.putText(frame, f"Reps: {counter}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        cv2.putText(frame, f"Sets: {sets}", (50, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Exercise Counter", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"✅ Final Repetition Count: {counter}")
print(f"✅ Total Sets Completed: {sets}")


# In[ ]:




