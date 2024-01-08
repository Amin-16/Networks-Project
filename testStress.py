import unittest
import socket
import threading
import json
import time

class TestStressSimulation(unittest.TestCase):
    def setUp(self):
        self.success_count = 0

    def simulate_client(self, username):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 5000))

        # Simulate login
        login_message = {
            "type": "login",
            "username": username,
            "password": "password"
        }
        client_socket.send(json.dumps(login_message).encode('utf-8'))

        # Simulate sending messages or performing other actions
        for i in range(10):
            time.sleep(1)
            message = {"type": "hello", "data": f"Message {i} from {username}"}
            client_socket.send(json.dumps(message).encode('utf-8'))

        # Simulate logout
        logout_message = {"type": "logout"}
        client_socket.send(json.dumps(logout_message).encode('utf-8'))

        # Close the socket
        client_socket.close()

        # Increment the success_count upon successful completion
        self.success_count += 1

    def test_stress_simulation(self):
        # Simulate 100 clients
        threads = []
        for i in range(100):
            username = f"user_{i}"
            thread = threading.Thread(target=self.simulate_client, args=(username,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Check if the stress test passed
        self.assertEqual(self.success_count, 100, "Stress test failed!")

if __name__ == "__main__":
    unittest.main()
