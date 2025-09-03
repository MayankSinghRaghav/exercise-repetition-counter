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

# Choose exercise type: "squat" or "jumpingjack"
EXERCISE = "squat"  

# Load video
cap = cv2.VideoCapture("one.mp4")

counter = 0
stage = None  # "up" / "down"

# Resize window for smooth display
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        if EXERCISE == "squat":
            # Track left hip and knee
            hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
            knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y

            # Rule: squat when hip goes below knee and then back up
            if hip > knee and stage != "down":
                stage = "down"
            if hip < knee and stage == "down":
                stage = "up"
                counter += 1

        elif EXERCISE == "jumpingjack":
            # Track hands relative to shoulders & hips
            left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
            right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y

            # Hands up → stage = "up"
            if left_hand < left_shoulder and right_hand < right_shoulder and stage != "up":
                stage = "up"

            # Hands down → count rep
            if left_hand > left_hip and right_hand > right_hip and stage == "up":
                stage = "down"
                counter += 1

        # Overlay reps on video
        cv2.putText(frame, f"{EXERCISE.capitalize()}s: {counter}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        # Draw pose landmarks
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # ✅ Resize frame for display
    frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    # Show video
    cv2.imshow("Exercise Counter", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"✅ Final {EXERCISE.capitalize()} Count: {counter}")


# In[ ]:




