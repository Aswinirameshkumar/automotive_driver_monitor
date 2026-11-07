import cv2
import numpy as np
import os
import urllib.request
import time

# URLs for Haar cascade files
face_cascade_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
eye_cascade_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye.xml"

face_cascade_file = "haarcascade_frontalface_default.xml"
eye_cascade_file = "haarcascade_eye.xml"

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            out_file.write(response.read())

download_file(face_cascade_url, face_cascade_file)
download_file(eye_cascade_url, eye_cascade_file)

face_cascade = cv2.CascadeClassifier(face_cascade_file)
eye_cascade = cv2.CascadeClassifier(eye_cascade_file)

# Initialize live webcam feed using DirectShow backend for Windows
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Could not open live webcam.")
    exit()

closed_eyes_counter = 0
DROWSY_THRESHOLD = 15
prev_time = 0

print("Starting Driver Monitoring System (Webcam Mode)... Press 'q' to exit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Warning: Lost frame feed from camera.")
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

        if len(eyes) == 0:
            closed_eyes_counter += 1
            if closed_eyes_counter >= DROWSY_THRESHOLD:
                cv2.putText(frame, "DROWSINESS ALERT! WAKE UP!", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            closed_eyes_counter = 0
            cv2.putText(frame, f"Eyes Detected: {len(eyes)} - Status: Alert", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # Calculate and display live FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
    prev_time = current_time

    cv2.putText(frame, f"FPS: {int(fps)}", (30, 95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Automotive Edge AI - Driver Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()