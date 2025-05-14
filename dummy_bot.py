#not used anymore
import time
import requests

BASE_URL = "http://127.0.0.1:8000"

def send_action(action):
    response = requests.post(f"{BASE_URL}/act", json={"action": action})
    print(f"Sent action: {action}, Response: {response.json()}")

def run_dummy_bot():
    while True:
        send_action("rotate_right")
        time.sleep(0.5)
        send_action("thrust")
        time.sleep(1.0)
        send_action("fire")
        time.sleep(2.0)
        send_action("stop_rotate")
        time.sleep(1.0)

if __name__ == "__main__":
    run_dummy_bot()
