import unittest
from unittest.mock import patch, Mock
import json
import urllib.error
from hubitat_client.rest_client import CloudRunRestClient

class TestCloudRunRestClient(unittest.TestCase):

    def setUp(self):
        # Arrange: Set up the base URL for all tests
        self.base_url = "https://example-run-service-url.run.app"
        self.client = CloudRunRestClient(self.base_url)
        self.resource = "test-resource"
        self.data = {"key": "value"}

    @patch("google.oauth2.id_token.fetch_id_token", return_value="test_token")
    @patch("urllib.request.urlopen")
    def test_get(self, mock_urlopen, mock_fetch_id_token):
        # Arrange: Mock the response from urlopen
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Act: Call the get method
        response = self.client.get(self.resource)

        # Assert: Verify that urlopen was called with the correct URL and method
        expected_url = f"{self.base_url}/{self.resource}"
        mock_urlopen.assert_called_once()
        self.assertIn(expected_url, mock_urlopen.call_args[0][0].full_url)
        self.assertEqual(response, json.dumps(self.data))

    @patch("google.oauth2.id_token.fetch_id_token", return_value="test_token")
    @patch("urllib.request.urlopen")
    def test_post(self, mock_urlopen, mock_fetch_id_token):
        # Arrange: Mock the response from urlopen
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Act: Call the post method
        response = self.client.post(self.resource, self.data)

        # Assert: Verify that urlopen was called with the correct URL, method, and data
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
        # Arrange: Mock the response from urlopen
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Act: Call the put method
        response = self.client.put(self.resource, self.data)

        # Assert: Verify that urlopen was called with the correct URL, method, and data
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
        # Arrange: Mock the response from urlopen
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.data).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Act: Call the delete method
        response = self.client.delete(self.resource)

        # Assert: Verify that urlopen was called with the correct URL and method
        expected_url = f"{self.base_url}/{self.resource}"
        mock_urlopen.assert_called_once()
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.full_url, expected_url)
        self.assertEqual(req.get_method(), "DELETE")
        self.assertEqual(response, json.dumps(self.data))

    @patch("google.oauth2.id_token.fetch_id_token", return_value="test_token")
    @patch("urllib.request.urlopen")
    def test_http_error_handling(self, mock_urlopen, mock_fetch_id_token):
        # Arrange: Mock an HTTPError
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url=self.base_url,
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=None,
        )

        # Act: Call the get method
        response = self.client.get(self.resource)

        # Assert: Verify that the correct error message is returned
        self.assertEqual(response, "HTTP Error: 404 - Not Found")

    @patch("google.oauth2.id_token.fetch_id_token", return_value="test_token")
    @patch("urllib.request.urlopen")
    def test_url_error_handling(self, mock_urlopen, mock_fetch_id_token):
        # Arrange: Mock a URLError
        mock_urlopen.side_effect = urllib.error.URLError("No internet connection")

        # Act: Call the get method
        response = self.client.get(self.resource)

        # Assert: Verify that the correct error message is returned
        self.assertEqual(response, "URL Error: No internet connection")


if __name__ == '__main__':
    unittest.main()
