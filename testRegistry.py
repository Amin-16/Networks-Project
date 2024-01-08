import unittest
from unittest.mock import patch, MagicMock
from registry import (
    handle_login,
    handle_create_account,
    handle_exit,
    handle_logout,
    handle_chatroom,
    handle_hello_udp,
    send_user_chatroom,
    broadcast_to_usernames,
)

class TestServerFunctionality(unittest.TestCase):

    @patch('database.P2PChatDB.verify_user_login')
    def test_handle_login_failure(self, mock_verify_user_login):
        conn = MagicMock()
        addr = ('127.0.0.1', 12345)
        message_data = {'type': 'login', 'username': 'test_user', 'password': 'test_password'}

        # Set up the mock database response
        mock_verify_user_login.return_value = False

        # Call the function
        handle_login(conn, message_data)

        # Assertions
        mock_verify_user_login.assert_called_once_with('test_user', 'test_password')
        conn.send.assert_called_once_with(b'{"type": "login_response", "status": "error", "msg": "Invalid username or password."}')

    # Add more tests for handle_create_account, handle_exit, handle_logout, handle_chatroom, etc.

    @patch('registry.broadcast_to_usernames')
    @patch('database.P2PChatDB.create_chatroom')
    def test_handle_chatroom_create(self, mock_create_chatroom, mock_broadcast):
        conn = MagicMock()
        addr = ('127.0.0.1', 12345)
        message_data = {'type': 'chatroom', 'method': 'create', 'users': ['user1', 'user2']}

        # Set up the mock database response
        mock_create_chatroom.return_value = {'_id': 'chatroom_id'}

        # Call the function
        handle_chatroom(conn, addr, message_data)

        # Assertions
        mock_create_chatroom.assert_called_once_with(['user1', 'user2'])
        mock_broadcast.assert_called_once_with(['user2'], {
            "type": "chatroom",
            "method": "invitation",
            "users": ['user1', 'user2'],
            "chatroom": {'_id': 'chatroom_id'},
        })


if __name__ == '__main__':
    unittest.main()
