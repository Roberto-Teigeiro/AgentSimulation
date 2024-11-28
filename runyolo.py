from ultralytics import YOLO
import cv2
import numpy as np
import mss

# Load the trained model
model = YOLO(r'C:\Users\ID140\Desktop\AgentSimulation\weights.onnx')

# Initialize MSS for screen capture
sct = mss.mss()

# Define the screen region to capture (full screen)
monitor = sct.monitors[1]  # 1 for primary monitor

while True:
    # Capture the screen
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)

    # Convert to BGR (mss captures in BGRA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # Perform inference
    results = model(frame)

    # Annotate frame with detections
    annotated_frame = results[0].plot()

    # Display the annotated frame
    cv2.imshow('YOLOv8 Real-Time Screen Detection', annotated_frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()