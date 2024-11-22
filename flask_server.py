from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# In-memory storage for agent positions
agent_positions = {}

@app.route('/update_position', methods=['POST'])
def update_position():
    data = request.get_json()
    agent_type = data.get('agent_type')
    position = data.get('position')
    
    if agent_type and position:
        # If position is a list, convert it to a dict
        if isinstance(position, list):
            if len(position) >= 2:
                position_dict = {'x': position[0], 'y': position[1]}
                # Optionally handle 'z' if a third element exists
                if len(position) >= 3:
                    position_dict['z'] = position[2]
                agent_positions[agent_type] = position_dict
                print(f"{agent_type} position updated: {position_dict}")
                return jsonify({'status': 'success'}), 200
            else:
                print(f"Invalid position list for {agent_type}: {position}")
                return jsonify({'status': 'failure', 'reason': 'Invalid position list length'}), 400
        # Ensure position is a dictionary with 'x' and 'y'
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

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()  # Get the JSON data sent from Unity
        image_data = data['image']  # Get the base64 image string

        # Decode the base64 string into bytes
        img_data = base64.b64decode(image_data)

        # Convert bytes into an image (using PIL or any other library)
        image = Image.open(BytesIO(img_data))

        # Optional: Save the image to a file (if needed)
        image.save("received_image.png")

        print("Received image")

        # Send a response to Unity (acknowledgment)
        return jsonify({"status": "success", "message": "Image received"}), 200
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"status": "error", "message": "Failed to process image"}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)