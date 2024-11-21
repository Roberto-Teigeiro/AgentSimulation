import time
import math
import requests

class Agent:
    def __init__(self, radius=5, speed=1):
        self.radius = radius  # Circle radius
        self.speed = speed    # Angular speed (radians per second)
        self.angle = 0        # Current angle (radians)

    def update_position(self):
        # Update the angle
        self.angle += self.speed * 0.1  # Adjust step size for smoothness
        self.angle %= 2 * math.pi       # Keep angle within [0, 2π]
        
        # Calculate the new position on the XZ plane (y stays constant)
        x = self.radius * math.cos(self.angle)
        z = self.radius * math.sin(self.angle)
        return {"x": x, "z": z, "angle": math.degrees(self.angle)}  # Return angle in degrees

if __name__ == "__main__":
    agent = Agent()
    server_url = "http://127.0.0.1:5000/update_position"
    update_interval = 0.1  # Send updates at 10 FPS

    while True:
        position = agent.update_position()
        try:
            # Send position and angle to Flask server
            response = requests.post(server_url, json=position)
            if response.status_code == 200:
                print("Position sent:", position)
            else:
                print("Failed to send position:", response.status_code, response.text)
        except Exception as e:
            print("Error sending data to server:", e)

        time.sleep(update_interval)  # 10 FPS
