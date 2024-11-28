from flask import Flask, request, jsonify, send_from_directory
import base64
from io import BytesIO
from PIL import Image
import os
import threading
import time
import requests
import random
import subprocess
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

# In-memory storage for agent positions
agent_positions = {}

# In-memory storage for alarm status
alarm_status = {'alarm_alerted': False, 'position': None}

# Define the folder to store images
IMAGE_FOLDER = 'agent_images'
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Load the trained model with explicit task definition
model = YOLO(r'C:\Users\ID140\Desktop\AgentSimulation\weights.onnx', task='detect')

@app.route('/update_position', methods=['POST'])
def update_position():
    data = request.get_json()
    agent_type = data.get('agent_type')
    position = data.get('position')
    
    if agent_type and position:
        if isinstance(position, list):
            if len(position) >= 2:
                position_dict = {'x': position[0], 'y': position[1]}
                if len(position) >= 3:
                    position_dict['z'] = position[2]
                agent_positions[agent_type] = position_dict
                print(f"{agent_type} position updated: {position_dict}")
                return jsonify({'status': 'success'}), 200
            else:
                print(f"Invalid position list for {agent_type}: {position}")
                return jsonify({'status': 'failure', 'reason': 'Invalid position list length'}), 400
        elif isinstance(position, dict) and 'x' in position and 'y' in position:
            agent_positions[agent_type] = position
            print(f"{agent_type} position updated: {position}")
            return jsonify({'status': 'success'}), 200
        else:
            print(f"Invalid position format for {agent_type}: {position}")
            return jsonify({'status': 'failure', 'reason': 'Invalid position format'}), 400
    else:
        return jsonify({'status': 'failure', 'reason': 'Invalid data'}), 400

@app.route('/get_positions', methods=['GET'])
def get_positions():
    return jsonify(agent_positions), 200

@app.route('/get_position/<agent_type>', methods=['GET'])
def get_position(agent_type):
    position = agent_positions.get(agent_type)
    if position:
        return jsonify(position), 200
    else:
        return jsonify({'error': f"Agent '{agent_type}' not found."}), 404

@app.route('/send_vision/<agent_type>', methods=['POST'])
def send_vision(agent_type):
    try:
        data = request.get_json()
        image_data = data.get('image')
        filename = data.get('filename', f"{agent_type}_vision.png")
        
        if not image_data:
            return jsonify({'status': 'failure', 'reason': 'No image data provided'}), 400
        
        # Decode the base64 string into bytes
        img_bytes = base64.b64decode(image_data)
        
        # Convert bytes into an image and save
        image = Image.open(BytesIO(img_bytes))
        file_path = os.path.join(IMAGE_FOLDER, f"{agent_type}_{filename}")
        image.save(file_path)
        
        print(f"Received and saved image for {agent_type}: {file_path}")
        return jsonify({'status': 'success', 'filename': f"{agent_type}_{filename}"}), 200
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to process image'}), 400

@app.route('/get_vision/<agent_type>/<filename>', methods=['GET'])
def get_vision(agent_type, filename):
    filename_with_agent = f"{agent_type}_{filename}"
    return send_from_directory(IMAGE_FOLDER, filename_with_agent)

@app.route('/start', methods=['POST'])
def start_simulation():
    def run_simulation():
        subprocess.run(["python", "DroneRobberSimulationV3.py"])

    # Run the simulation in a separate thread to avoid blocking the Flask server
    simulation_thread = threading.Thread(target=run_simulation)
    simulation_thread.start()
    
    return jsonify({'status': 'simulation started'}), 200

@app.route('/alert_alarm', methods=['POST'])
def alert_alarm():
    data = request.get_json()
    alarm_status['alarm_alerted'] = data.get('alarm_alerted', False)
    alarm_status['position'] = data.get('position', None)
    print(f"Alarm status updated: {alarm_status['alarm_alerted']}, Position: {alarm_status['position']}")
    return jsonify({'status': 'success'}), 200

@app.route('/alarm_status', methods=['GET'])
def get_alarm_status():
    return jsonify(alarm_status), 200

@app.route('/check_image/<camera_name>', methods=['POST'])
def check_image(camera_name):
    try:
        # Construct the filename based on the camera name
        filename = f"{camera_name}_{camera_name}_vision.png"
        image_path = os.path.join(IMAGE_FOLDER, filename)
        
        if not os.path.exists(image_path):
            return jsonify({'status': 'failure', 'reason': 'Image not found'}), 404
        
        # Load the image
        frame = cv2.imread(image_path)

        # Perform inference
        results = model(frame)

        # Annotate frame with detections
        annotated_frame = results[0].plot()

        # Save the annotated frame to a file
        output_path = os.path.join(IMAGE_FOLDER, f"{camera_name}_annotated.png")
        cv2.imwrite(output_path, annotated_frame)
        print(f"Annotated image saved to: {output_path}")

        # Check if any objects are detected
        if results[0].boxes:
            return jsonify({'status': 'success', 'sus_object_detected': True, 'annotated_image': output_path}), 200
        else:
            return jsonify({'status': 'success', 'sus_object_detected': False, 'annotated_image': output_path}), 200
    except Exception as e:
        print(f"Error checking image: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to check image'}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)