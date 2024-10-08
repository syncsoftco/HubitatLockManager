import urllib
import google.auth.transport.requests
import google.oauth2.id_token
import json

class CloudRunRestClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.audience = base_url

    def _get_id_token(self):
        auth_req = google.auth.transport.requests.Request()
        return google.oauth2.id_token.fetch_id_token(auth_req, self.audience)

    def _make_request(self, method, resource, data=None):
        url = f"{self.base_url}/{resource}"
        req = urllib.request.Request(url, method=method.upper())

        if data:
            req.add_header("Content-Type", "application/json")
            req.data = json.dumps(data).encode('utf-8')

        req.add_header("Authorization", f"Bearer {self._get_id_token()}")

        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')

    def get(self, resource):
        return self._make_request('GET', resource)

    def post(self, resource, data):
        return self._make_request('POST', resource, data)

    def put(self, resource, data):
        return self._make_request('PUT', resource, data)

    def delete(self, resource):
        return self._make_request('DELETE', resource)
