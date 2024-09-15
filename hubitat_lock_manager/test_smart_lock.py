import unittest
from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import List

# Update the import statement to use the correct module
from hubitat_lock_manager.smart_lock import (
    SmartLock, CreateKeyCodeParams, DeleteKeyCodeParams, LockCode,
    ListKeyCodesResult, CreateKeyCodeResult, DeleteKeyCodeResult,
    create_generic_z_wave_lock, get_next_position_based_on_list_key_codes_result,
    WebdriverConfig, create_webdriver_based_code_lister,
    create_webdriver_based_code_setter, create_webdriver_based_code_deleter
)

class TestSmartLock(unittest.TestCase):
    def setUp(self):
        self.mock_position_deleter = Mock()
        self.mock_code_lister = Mock()
        self.mock_code_setter = Mock()
        
        self.smart_lock = create_generic_z_wave_lock(
            device_id=1,
            position_deleter=self.mock_position_deleter,
            code_lister=self.mock_code_lister,
            code_setter=self.mock_code_setter
        )

    def test_create_key_code_success(self):
        # Arrange
        params = CreateKeyCodeParams(code="1234", username="testuser")
        self.mock_code_lister.list_codes.return_value = ListKeyCodesResult(codes=[])
        self.mock_code_setter.set_code.return_value = Mock(position=1)

        # Act
        result = self.smart_lock.create_key_code(params)

        # Assert
        self.assertIsInstance(result, CreateKeyCodeResult)
        self.assertEqual(result.position, 1)
        self.assertIsNotNone(result.timestamp)
        self.mock_code_setter.set_code.assert_called_once()

    def test_create_key_code_duplicate_code(self):
        # Arrange
        params = CreateKeyCodeParams(code="1234", username="testuser")
        self.mock_code_lister.list_codes.return_value = ListKeyCodesResult(
            codes=[LockCode(code="1234", name="existinguser", position=1)]
        )

        # Act & Assert
        with self.assertRaises(ValueError):
            self.smart_lock.create_key_code(params)

    def test_delete_key_code_success(self):
        # Arrange
        params = DeleteKeyCodeParams(username="testuser")
        self.mock_code_lister.list_codes.return_value = ListKeyCodesResult(
            codes=[LockCode(code="1234", name="testuser", position=1)]
        )

        # Act
        result = self.smart_lock.delete_key_code(params)

        # Assert
        self.assertIsInstance(result, DeleteKeyCodeResult)
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Key code deleted")
        self.mock_position_deleter.delete_position.assert_called_once()

    def test_delete_key_code_not_found(self):
        # Arrange
        params = DeleteKeyCodeParams(username="nonexistent")
        self.mock_code_lister.list_codes.return_value = ListKeyCodesResult(codes=[])

        # Act
        result = self.smart_lock.delete_key_code(params)

        # Assert
        self.assertIsInstance(result, DeleteKeyCodeResult)
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Key code not found")
        self.mock_position_deleter.delete_position.assert_not_called()

    def test_list_key_codes(self):
        # Arrange
        expected_codes = [LockCode(code="1234", name="user1", position=1)]
        self.mock_code_lister.list_codes.return_value = ListKeyCodesResult(codes=expected_codes)

        # Act
        result = self.smart_lock.list_key_codes()

        # Assert
        self.assertIsInstance(result, ListKeyCodesResult)
        self.assertEqual(result.codes, expected_codes)
        self.mock_code_lister.list_codes.assert_called_once()

class TestWebdriverBasedComponents(unittest.TestCase):
    @patch('hubitat_lock_manager.smart_lock.webdriver.Chrome')
    def test_webdriver_based_code_deleter(self, mock_chrome):
        # Arrange
        config = WebdriverConfig(hub_ip="192.168.1.100", command_executor="")
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_form = Mock()
        mock_driver.find_element.return_value = mock_form
        
        deleter = create_webdriver_based_code_deleter(device_id=1, config=config)

        # Act
        deleter.delete_position(Mock(position=1))

        # Assert
        mock_driver.get.assert_called_once_with("http://192.168.1.100/device/edit/1")
        mock_driver.find_element.assert_called_once()
        mock_form.find_element.assert_called_once()
        mock_form.submit.assert_called_once()
        mock_driver.quit.assert_called_once()

    @patch('hubitat_lock_manager.smart_lock.webdriver.Chrome')
    def test_webdriver_based_code_lister(self, mock_chrome):
        # Arrange
        config = WebdriverConfig(hub_ip="192.168.1.100", command_executor="")
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_element = Mock()
        mock_element.get_attribute.return_value = '{"1": {"code": "1234", "name": "user1"}}'
        mock_driver.find_element.return_value = mock_element
        
        lister = create_webdriver_based_code_lister(config)

        # Act
        result = lister.list_codes(device_id=1)

        # Assert
        self.assertIsInstance(result, ListKeyCodesResult)
        self.assertEqual(len(result.codes), 1)
        self.assertEqual(result.codes[0].code, "1234")
        self.assertEqual(result.codes[0].name, "user1")
        self.assertEqual(result.codes[0].position, 1)
        mock_driver.get.assert_called_once_with("http://192.168.1.100/device/edit/1")
        mock_driver.quit.assert_called_once()

    @patch('hubitat_lock_manager.smart_lock.webdriver.Chrome')
    def test_webdriver_based_code_setter(self, mock_chrome):
        # Arrange
        config = WebdriverConfig(hub_ip="192.168.1.100", command_executor="")
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_form = Mock()
        mock_driver.find_element.return_value = mock_form
        
        setter = create_webdriver_based_code_setter(device_id=1, config=config)

        # Act
        result = setter.set_code(Mock(code="5678", name="newuser"))

        # Assert
        self.assertIsInstance(result, SetCodeResult)
        mock_driver.get.assert_called_once_with("http://192.168.1.100/device/edit/1")
        mock_driver.find_element.assert_called_once()
        self.assertEqual(mock_form.find_element.call_count, 3)  # Three input fields
        mock_form.submit.assert_called_once()
        mock_driver.quit.assert_called_once()

class TestHelperFunctions(unittest.TestCase):
    def test_get_next_position_based_on_list_key_codes_result(self):
        # Arrange
        codes = [
            LockCode(code="1111", name="user1", position=1),
            LockCode(code="2222", name="user2", position=2),
            LockCode(code="3333", name="user3", position=4)
        ]
        result = ListKeyCodesResult(codes=codes)

        # Act
        next_position = get_next_position_based_on_list_key_codes_result(result)

        # Assert
        self.assertEqual(next_position, 3)

if __name__ == '__main__':
    unittest.main()
