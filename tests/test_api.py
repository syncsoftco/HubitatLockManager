import unittest
from unittest.mock import patch, MagicMock
from flask import json
from hubitat_lock_manager.api import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('hubitat_lock_manager.controller.SmartLockController')
    def test_create_key_code_success(self, MockSmartLockController):
        # Mock the SmartLockController instance
        mock_controller = MockSmartLockController.return_value
        mock_controller.create_key_code.return_value = [
            MagicMock(code='1234', username='user1', device_id=1)
        ]

        # Send POST request
        response = self.app.post('/create_key_code', data=json.dumps({
            'code': '1234',
            'username': 'user1',
            'device_id': 1
        }), content_type='application/json')

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'code': '1234', 'username': 'user1', 'device_id': 1}])

        # Verify that the method was called with the expected parameters
        mock_controller.create_key_code.assert_called_once_with(mock_controller.CreateKeyCodeParams(
            code='1234',
            username='user1',
            device_id=1
        ))

    @patch('hubitat_lock_manager.controller.SmartLockController')
    def test_create_key_code_failure(self, MockSmartLockController):
        # Mock the SmartLockController to raise an exception
        mock_controller = MockSmartLockController.return_value
        mock_controller.create_key_code.side_effect = Exception("Test Exception")

        # Send POST request
        response = self.app.post('/create_key_code', data=json.dumps({
            'code': '1234',
            'username': 'user1',
            'device_id': 1
        }), content_type='application/json')

        # Check response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Test Exception"})

        # Verify that the method was called with the expected parameters
        mock_controller.create_key_code.assert_called_once_with(mock_controller.CreateKeyCodeParams(
            code='1234',
            username='user1',
            device_id=1
        ))

    @patch('hubitat_lock_manager.controller.SmartLockController')
    def test_delete_key_code_success(self, MockSmartLockController):
        # Mock the SmartLockController instance
        mock_controller = MockSmartLockController.return_value
        mock_controller.delete_key_code.return_value = MagicMock(username='user1', device_id=1)

        # Send DELETE request
        response = self.app.delete('/delete_key_code', data=json.dumps({
            'username': 'user1',
            'device_id': 1
        }), content_type='application/json')

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'username': 'user1', 'device_id': 1})

        # Verify that the method was called with the expected parameters
        mock_controller.delete_key_code.assert_called_once_with('user1', 1)

    @patch('hubitat_lock_manager.controller.SmartLockController')
    def test_list_devices_success(self, MockSmartLockController):
        # Mock the SmartLockController instance
        mock_controller = MockSmartLockController.return_value
        mock_controller.list_devices.return_value = MagicMock(devices=[{'id': 1, 'name': 'Front Door'}])

        # Send GET request
        response = self.app.get('/list_devices')

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'devices': [{'id': 1, 'name': 'Front Door'}]})

        # Verify that the method was called
        mock_controller.list_devices.assert_called_once()

    @patch('hubitat_lock_manager.controller.SmartLockController')
    def test_list_key_codes_success(self, MockSmartLockController):
        # Mock the SmartLockController instance
        mock_controller = MockSmartLockController.return_value
        mock_controller.list_key_codes.return_value = MagicMock(codes=[{'code': '1234', 'username': 'user1'}])

        # Send GET request
        response = self.app.get('/list_key_codes?device_id=1')

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'codes': [{'code': '1234', 'username': 'user1'}]})

        # Verify that the method was called with the expected parameters
        mock_controller.list_key_codes.assert_called_once_with(1)

    @patch('hubitat_lock_manager.controller.SmartLockController')
    def test_list_key_codes_failure(self, MockSmartLockController):
        # Send GET request without device_id
        response = self.app.get('/list_key_codes')

        # Check response
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
