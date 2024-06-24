import unittest
from unittest.mock import MagicMock
from hubitat_lock_manager.models import CreateKeyCodeParams, UpdateKeyCodeParams, DeleteKeyCodeParams, ReadKeyCodeParams
from hubitat_lock_manager.smart_lock import create_yale_assure_lever
from hubitat_lock_manager.batch_job import init_batch_job, run_batch_job, hash_request
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver

class TestSmartLockManager(unittest.TestCase):
    def setUp(self):
        self.driver = MagicMock(WebDriver, desired_capabilities=DesiredCapabilities.CHROME)
        self.smart_lock = create_yale_assure_lever(self.driver)

    def test_create_key_code(self):
        params = CreateKeyCodeParams(lock_id="lock123", code="1234", name="Test Code")
        result = self.smart_lock.create_key_code(params)
        self.assertTrue(result.success)

    def test_update_key_code(self):
        params = UpdateKeyCodeParams(lock_id="lock123", code_id="code123", new_code="4321", new_name="Updated Code")
        result = self.smart_lock.update_key_code(params)
        self.assertTrue(result.success)

    def test_delete_key_code(self):
        params = DeleteKeyCodeParams(lock_id="lock123", code_id="code123")
        result = self.smart_lock.delete_key_code(params)
        self.assertTrue(result.success)

    def test_read_key_code(self):
        params = ReadKeyCodeParams(lock_id="lock123", code_id="code123")
        result = self.smart_lock.read_key_code(params)
        self.assertEqual(result.code, "1234")

    def test_list_key_codes(self):
        result = self.smart_lock.list_key_codes("lock123")
        self.assertTrue(len(result.codes) > 0)

class TestBatchJob(unittest.TestCase):
    def setUp(self):
        self.driver_path = "path/to/chromedriver"
        self.hubitat_url = "http://hubitat.local"
        self.username = "user"
        self.password = "pass"
        self.db_connection = MagicMock()

        self.batch_job = init_batch_job(self.driver_path, self.hubitat_url, self.username, self.password, self.db_connection)

    def test_hash_request(self):
        timestamp = 1625079650.0
        code = "1234"
        name = "Test Code"
        expected_hash = "2c4a6d8fb9e1e70c13b1f4670c453e8f9dbdf2a9127322bbf1914e4721687305"
        self.assertEqual(hash_request(timestamp, code, name), expected_hash)

    def test_run_batch_job(self):
        self.batch_job.data_store.get_pending_key_codes.return_value = [
            {"lock_id": "lock123", "code": "1234", "name": "Test Code", "timestamp": 1625079650.0}
        ]
        self.batch_job.data_store.is_request_processed.return_value = False

        run_batch_job(self.batch_job)

        self.batch_job.data_store.record_key_code_result.assert_called_once()

if __name__ == '__main__':
    unittest.main()
