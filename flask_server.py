from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

agent_data = {"x": 0, "z": 0, "angle": 0}  # Include angle in the data

@app.route('/update_position', methods=['POST'])
def update_position():
    global agent_data
    data = request.get_json()
    if "x" in data and "z" in data and "angle" in data:
        agent_data = data
        return jsonify({"status": "success", "data": agent_data}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/position', methods=['GET'])
def get_position():
    return jsonify(agent_data)

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

@app.route('/get_image', methods=['GET'])
def get_image():
    # Open the saved image and send it as an HTTP response
    with open("received_image.png", "rb") as f:
        image_data = f.read()
    return image_data, 200, {'Content-Type': 'image/png'}

if __name__ == "__main__":
    app.run(debug=True)
