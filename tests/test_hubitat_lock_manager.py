import unittest
from unittest.mock import MagicMock
from hubitat_lock_manager.models import CreateKeyCodeParams, UpdateKeyCodeParams, DeleteKeyCodeParams
from hubitat_lock_manager.smart_lock import create_yale_assure_lever
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver

class TestSmartLockManager(unittest.TestCase):
    def setUp(self):
        self.driver = MagicMock(WebDriver, desired_capabilities=DesiredCapabilities.CHROME)
        self.smart_lock = create_yale_assure_lever(self.driver)

    def test_create_key_code(self):
        params = CreateKeyCodeParams(code="1234", name="Test Code")
        result = self.smart_lock.create_key_code(params)
        self.assertTrue(result.success)

    def test_update_key_code(self):
        params = UpdateKeyCodeParams(old_code="1234", new_code="4321", new_name="Updated Code")
        result = self.smart_lock.update_key_code(params)
        self.assertTrue(result.success)

    def test_delete_key_code(self):
        params = DeleteKeyCodeParams(code="1234")
        result = self.smart_lock.delete_key_code(params)
        self.assertTrue(result.success)

    def test_list_key_codes(self):
        result = self.smart_lock.list_key_codes()
        self.assertTrue(len(result.codes) > 0)

if __name__ == '__main__':
    unittest.main()
