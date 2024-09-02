import unittest
from unittest.mock import patch, Mock
import json
import urllib.error
from hubitat_lock_manager.rest_client import CloudRunRestClient

class TestCloudRunRestClient(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://example-run-service-url.run.app"
        self.client = CloudRunRestClient(self.base_url)
        self.resource = "test-resource"
        self.data = {"key": "value"}

    @patch("google.oauth2.id_token.fetch_id_token", return_value="test_token")
    @patch("urllib.request.urlopen")
    def test_get(self, mock_urlopen, mock_fetch_id_token):
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.data).encode('utf-8')
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Act
        response = self.client.get(self.resource)

        # Assert
        expected_url = f"{self.base_url}/{self.resource}"
        mock_urlopen.assert_called_once()
        self.assertIn(expected_url, mock_urlopen.call_args[0][0].full_url)
        self.assertEqual(response, json.dumps(self.data))

    @patch("google.oauth2.id_token.fetch_id_token", return_value="test_token")
    @patch("urllib.request.urlopen")
    def test_post(self, mock_urlopen, mock_fetch_id_token):
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.data).encode('utf-8')
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Act
        response = self.client.post(self.resource, self.data)

        # Assert
        expected_url = f"{self.base_url}/{self.resource}"
        mock_urlopen.assert_called_once()
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.full_url, expected_url)
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(req.data, json.dumps(self.data).encode('utf-8'))
        self.assertEqual(response, json.dumps(self.data))

    @patch("google.oauth2.id_token.fetch_id_token", return_value="test_token")
    @patch("urllib.request.urlopen")
    def test_put(self, mock_urlopen, mock_fetch_id_token):
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.data).encode('utf-8')
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Act
        response = self.client.put(self.resource, self.data)

        # Assert
        expected_url = f"{self.base_url}/{self.resource}"
        mock_urlopen.assert_called_once()
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.full_url, expected_url)
        self.assertEqual(req.get_method(), "PUT")
        self.assertEqual(req.data, json.dumps(self.data).encode('utf-8'))
        self.assertEqual(response, json.dumps(self.data))

    @patch("google.oauth2.id_token.fetch_id_token", return_value="test_token")
    @patch("urllib.request.urlopen")
    def test_delete(self, mock_urlopen, mock_fetch_id_token):
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.data).encode('utf-8')
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Act
        response = self.client.delete(self.resource)

        # Assert
        expected_url = f"{self.base_url}/{self.resource}"
        mock_urlopen.assert_called_once()
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.full_url, expected_url)
        self.assertEqual(req.get_method(), "DELETE")
        self.assertEqual(response, json.dumps(self.data))


if __name__ == '__main__':
    unittest.main()
