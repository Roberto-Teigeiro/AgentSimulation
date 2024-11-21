import time
import math
import requests
import agentpy as ap

class Agent(ap.Agent):
    def __init__(self, environment, radius=5, speed=1):
        super().__init__(environment)
        self.radius = radius  # Circle radius
        self.speed = speed    # Angular speed (radians per second)
        self.angle = 0        # Current angle (radians)

    def update_position(self):
        self.angle += self.speed * 0.1  # Adjust step size for smoothness
        self.angle %= 2 * math.pi       # Keep angle within [0, 2π]
        x = self.radius * math.cos(self.angle)
        z = self.radius * math.sin(self.angle)
        time.sleep(1)
        return {"x": x, "z": z, "angle": math.degrees(self.angle)}  # Angle in degrees

class MyModel(ap.Model):
    def setup(self):
        self.agent = Agent(self)
        self.server_url = "http://127.0.0.1:5000/update_position"
        self.update_interval = 1  # 10 FPS

    def step(self):
        position = self.agent.update_position()
        try:
            response = requests.post(self.server_url, json=position)
            if response.status_code == 200:
                print("Position sent: {}".format(position))
            else:
                print("Failed to send position: {} {}".format(response.status_code, response.text))
        except Exception as e:
            print("Error sending data to server: {}".format(e))

if __name__ == "__main__":
    model = MyModel()
    model.run(steps=30)