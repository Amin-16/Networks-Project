import unittest
from unittest.mock import patch
from peer import PeerServer  # Replace with the actual module where PeerServer is defined
from peer import create_and_connect_client, send_login, send_create_account, start_hello_thread

class TestChatroomFunctionality(unittest.TestCase):

    def setUp(self):
        # Set up any necessary resources or configurations before each test
        self.client = None

    def tearDown(self):
        # Clean up any resources or configurations after each test
        if self.client:
            self.client.close()

    def test_chatroom_creation_and_joining(self):
        # Mock the server connection for testing
        with patch('peer.socket') as mock_socket:
            # Mock the server response for login
            mock_socket.return_value.recv.return_value.decode.return_value = '{"type": "login_response", "status": "ok"}'

            # Create and connect the client
            create_and_connect_client()

            # Mock the server response for creating a chatroom
            mock_socket.return_value.recv.return_value.decode.return_value = '{"type": "chatroom", "method": "create", "status": "ok"}'

            # Send login request
            self.assertTrue(send_login("test_user", "test_password"))

            # Start the hello thread
            start_hello_thread()

            # Mock the server response for getting chatrooms
            mock_socket.return_value.recv.return_value.decode.return_value = '{"type": "chatroom", "method": "get all", "chatrooms": [{"_id": {"$oid": "123"}, "usernames": ["test_user"]}]}'


            # Mock the server response for joining a chatroom
            mock_socket.return_value.recv.return_value.decode.return_value = '{"type": "chatroom", "method": "join", "status": "ok"}'

            # Mock the PeerServer class
            with patch('peer.PeerServer'):
                # Join a chatroom
                self.assertTrue(self.client.join_chatroom("123"))

                # Add your assertions based on the expected behavior
                # For example, check if the user is now part of the chatroom, etc.

if __name__ == '__main__':
    unittest.main()
