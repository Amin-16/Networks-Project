import unittest
from unittest.mock import patch, MagicMock
from peer import join_one2one

class TestOneToOneChat(unittest.TestCase):

    @patch('builtins.input', side_effect=['message 1', 'message 2', ':q'])
    def test_one_to_one_chat(self, mock_input):
        # Mock necessary components
        mock_send_message = MagicMock()

        # Mock the chatPeer for user1
        mock_chat_peer_user1 = {'username': 'user1', 'address': {'portRecv': 1234}}

        # Mock the chatPeer for user2
        mock_chat_peer_user2 = {'username': 'user2', 'address': {'portRecv': 5678}}

        with patch('peer.send_message', mock_send_message):
            # Set up the test environment for user1
            with patch('peer.isChatting', side_effect=[True, True, False]), \
                    patch('peer.chatPeer', mock_chat_peer_user1):
                # Run the function to be tested for user1
                join_one2one(mock_chat_peer_user1, 'test_user')

        # Assertions for user1
        mock_send_message.assert_any_call(None, username='test_user', userReciever=mock_chat_peer_user1, message='message 1')
        mock_send_message.assert_any_call(None, username='test_user', userReciever=mock_chat_peer_user1, message='message 2')
        mock_send_message.assert_any_call(None, username='test_user', userReciever=mock_chat_peer_user1, message=':q')

        # Reset mock for user2
        mock_send_message.reset_mock()

        with patch('peer.send_message', mock_send_message):
            # Set up the test environment for user2
            with patch('peer.isChatting', side_effect=[True, False]), \
                    patch('peer.chatPeer', mock_chat_peer_user2):
                # Run the function to be tested for user2
                join_one2one(mock_chat_peer_user2, 'test_user2')

        # Assertions for user2
        mock_send_message.assert_any_call(None, username='test_user2', userReciever=mock_chat_peer_user2, message='message 1')
        mock_send_message.assert_any_call(None, username='test_user2', userReciever=mock_chat_peer_user2, message='message 2')
        mock_send_message.assert_any_call(None, username='test_user2', userReciever=mock_chat_peer_user2, message=':q')


if __name__ == '__main__':
    unittest.main()

