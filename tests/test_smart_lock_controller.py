import unittest
from unittest.mock import patch, MagicMock
from hubitat_lock_manager.controller import SmartLockController
from hubitat_lock_manager.factory import SmartLockFactory
from hubitat_lock_manager.models import CreateKeyCodeParams, UpdateKeyCodeParams, DeleteKeyCodeParams, CreateKeyCodeResult, UpdateKeyCodeResult, DeleteKeyCodeResult, ListKeyCodesResult

class TestSmartLockController(unittest.TestCase):
    def setUp(self):
        self.factory = SmartLockFactory.TEST_FACTORY
        self.controller = SmartLockController(self.factory)
        self.driver_patch = patch('hubitat_lock_manager.controller.webdriver.Chrome')
        self.driver_mock = self.driver_patch.start()

    def tearDown(self):
        self.driver_patch.stop()

    @patch('hubitat_lock_manager.controller.HubitatManager')
    def test_create_key_code(self, HubitatManagerMock):
        create_result = CreateKeyCodeResult(success=True, message="Key code created")
        smart_lock_mock = MagicMock()
        smart_lock_mock.create_key_code.return_value = create_result

        manager_mock = HubitatManagerMock.return_value.__enter__.return_value
        manager_mock.create_key_code.return_value = create_result

        params = CreateKeyCodeParams(code="1234", name="Test Code")
        result = self.controller.create_key_code(params)

        self.assertTrue(result.success)
        self.assertEqual(result.message, "Key code created")

    @patch('hubitat_lock_manager.controller.HubitatManager')
    def test_update_key_code(self, HubitatManagerMock):
        update_result = UpdateKeyCodeResult(success=True, message="Key code updated")
        smart_lock_mock = MagicMock()
        smart_lock_mock.update_key_code.return_value = update_result

        manager_mock = HubitatManagerMock.return_value.__enter__.return_value
        manager_mock.update_key_code.return_value = update_result

        params = UpdateKeyCodeParams(old_code="1234", new_code="4321", new_name="Updated Code")
        result = self.controller.update_key_code(params)

        self.assertTrue(result.success)
        self.assertEqual(result.message, "Key code updated")

    @patch('hubitat_lock_manager.controller.HubitatManager')
    def test_delete_key_code(self, HubitatManagerMock):
        delete_result = DeleteKeyCodeResult(success=True, message="Key code deleted")
        smart_lock_mock = MagicMock()
        smart_lock_mock.delete_key_code.return_value = delete_result

        manager_mock = HubitatManagerMock.return_value.__enter__.return_value
        manager_mock.delete_key_code.return_value = delete_result

        params = DeleteKeyCodeParams(code="1234")
        result = self.controller.delete_key_code(params)

        self.assertTrue(result.success)
        self.assertEqual(result.message, "Key code deleted")

    @patch('hubitat_lock_manager.controller.HubitatManager')
    def test_list_key_codes(self, HubitatManagerMock):
        list_result = ListKeyCodesResult(codes=[CreateKeyCodeParams(code="1234", name="Test Code")])
        smart_lock_mock = MagicMock()
        smart_lock_mock.list_key_codes.return_value = list_result

        manager_mock = HubitatManagerMock.return_value.__enter__.return_value
        manager_mock.list_key_codes.return_value = list_result

        result = self.controller.list_key_codes()

        self.assertEqual(len(result.codes), 1)
        self.assertEqual(result.codes[0].code, "1234")
        self.assertEqual(result.codes[0].name, "Test Code")

if __name__ == '__main__':
    unittest.main()
