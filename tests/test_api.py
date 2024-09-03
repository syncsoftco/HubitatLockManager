import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import json

from hubitat_lock_manager import controller
from hubitat_lock_manager.api import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("hubitat_lock_manager.controller.smart_lock_controller.create_key_code")
    def test_create_key_code_success(self, mock_create_key_code):
        # Arrange
        mock_result = MagicMock()
        mock_result.username = "testuser"
        mock_result.device_id = 123
        mock_result.code = "1234"
        mock_create_key_code.return_value = [mock_result]

        payload = {
            "code": "1234",
            "username": "testuser",
            "device_id": 123
        }

        # Act
        response = self.app.post("/create_key_code", json=payload)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{
            "username": "testuser",
            "device_id": 123,
            "code": "1234"
        }])
        mock_create_key_code.assert_called_once()

    @patch("hubitat_lock_manager.controller.smart_lock_controller.create_key_code")
    def test_create_key_code_failure(self, mock_create_key_code):
        # Arrange
        mock_create_key_code.side_effect = Exception("Creation failed")

        payload = {
            "code": "1234",
            "username": "testuser",
            "device_id": 123
        }

        # Act
        response = self.app.post("/create_key_code", json=payload)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Creation failed"})
        mock_create_key_code.assert_called_once()

    @patch("hubitat_lock_manager.controller.smart_lock_controller.delete_key_code")
    def test_delete_key_code_success(self, mock_delete_key_code):
        # Arrange
        mock_result = MagicMock()
        mock_result.username = "testuser"
        mock_result.device_id = 123
        mock_delete_key_code.return_value = mock_result

        payload = {
            "username": "testuser",
            "device_id": 123
        }

        # Act
        response = self.app.delete("/delete_key_code", json=payload)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "username": "testuser",
            "device_id": 123
        })
        mock_delete_key_code.assert_called_once_with("testuser", 123)

    @patch("hubitat_lock_manager.controller.smart_lock_controller.delete_key_code")
    def test_delete_key_code_failure(self, mock_delete_key_code):
        # Arrange
        mock_delete_key_code.side_effect = Exception("Deletion failed")

        payload = {
            "username": "testuser",
            "device_id": 123
        }

        # Act
        response = self.app.delete("/delete_key_code", json=payload)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Deletion failed"})
        mock_delete_key_code.assert_called_once_with("testuser", 123)

    @patch("hubitat_lock_manager.controller.smart_lock_controller.list_devices")
    def test_list_devices_success(self, mock_list_devices):
        # Arrange
        mock_result = MagicMock()
        mock_list_devices.return_value = mock_result

        # Act
        response = self.app.get("/list_devices")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})
        mock_list_devices.assert_called_once()

    @patch("hubitat_lock_manager.controller.smart_lock_controller.list_devices")
    def test_list_devices_failure(self, mock_list_devices):
        # Arrange
        mock_list_devices.side_effect = Exception("Internal error")

        # Act
        response = self.app.get("/list_devices")

        # Assert
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Internal server error"})
        mock_list_devices.assert_called_once()

    @patch("hubitat_lock_manager.controller.smart_lock_controller.list_key_codes")
    def test_list_key_codes_success(self, mock_list_key_codes):
        # Arrange
        mock_result = MagicMock()
        mock_list_key_codes.return_value = mock_result

        # Act
        response = self.app.get("/list_key_codes", query_string={"device_id": 123})

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})
        mock_list_key_codes.assert_called_once_with(123)

    @patch("hubitat_lock_manager.controller.smart_lock_controller.list_key_codes")
    def test_list_key_codes_failure(self, mock_list_key_codes):
        # Arrange
        mock_list_key_codes.side_effect = Exception("List failed")

        # Act
        response = self.app.get("/list_key_codes", query_string={"device_id": 123})

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "List failed"})
        mock_list_key_codes.assert_called_once_with(123)


if __name__ == "__main__":
    unittest.main()
