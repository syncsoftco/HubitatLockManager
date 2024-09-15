import unittest
from unittest import TestCase
from unittest.mock import patch, Mock
from typing import List
import time

from hubitat_lock_manager import smart_lock


# Fake implementations of the test doubles
class FakePositionDeleter(smart_lock.PositionDeleter):
    def __init__(self):
        self.deleted_positions = []

    def delete_position(self, params: smart_lock.DeletePositionParams) -> None:
        self.deleted_positions.append(params.position)


class FakeCodeLister(smart_lock.CodeLister):
    def __init__(self, codes=None):
        if codes is None:
            codes = []
        self.codes = codes

    def list_codes(self, device_id: int) -> smart_lock.ListKeyCodesResult:
        return smart_lock.ListKeyCodesResult(codes=self.codes)


class FakeCodeSetter(smart_lock.CodeSetter):
    def __init__(self):
        self.codes = []
        self.next_position = 1

    def get_next_position(self) -> int:
        return self.next_position

    def set_code(self, params: smart_lock.SetCodeParams) -> smart_lock.SetCodeResult:
        position = self.get_next_position()
        self.codes.append(smart_lock.LockCode(params.code, params.name, position))
        self.next_position += 1
        return smart_lock.SetCodeResult(position)


# Test case implementation
class TestSmartLock(TestCase):
    def setUp(self):
        # Arrange
        self.device_id = 1
        self.fake_position_deleter = FakePositionDeleter()
        self.fake_code_lister = FakeCodeLister()
        self.fake_code_setter = FakeCodeSetter()

        self.sut = smart_lock.create_generic_z_wave_lock(
            self.device_id,
            self.fake_position_deleter,
            self.fake_code_lister,
            self.fake_code_setter,
        )

    def test_create_key_code_success(self):
        # Arrange
        params = smart_lock.CreateKeyCodeParams(code="1234", username="test_user")

        # Act
        result = self.sut.create_key_code(params)

        # Assert
        self.assertEqual(result.position, 1)
        self.assertGreater(result.timestamp, 0)
        self.assertIn("1234", [code.code for code in self.fake_code_setter.codes])
        self.assertEqual(self.fake_code_setter.codes[0].name, "test_user")

    def test_create_key_code_duplicate_code(self):
        # Arrange
        self.fake_code_lister.codes = [
            smart_lock.LockCode(code="1234", name="user1", position=1)
        ]
        params = smart_lock.CreateKeyCodeParams(code="1234", username="test_user")

        # Act / Assert
        with self.assertRaises(ValueError) as context:
            self.sut.create_key_code(params)
        self.assertEqual(str(context.exception), "Code 1234 already exists")

    def test_create_key_code_duplicate_username(self):
        # Arrange
        self.fake_code_lister.codes = [
            smart_lock.LockCode(code="5678", name="test_user", position=1)
        ]
        params = smart_lock.CreateKeyCodeParams(code="1234", username="test_user")

        # Act / Assert
        with self.assertRaises(ValueError) as context:
            self.sut.create_key_code(params)
        self.assertEqual(str(context.exception), "Key code for test_user already exists")

    def test_delete_key_code_success(self):
        # Arrange
        self.fake_code_lister.codes = [
            smart_lock.LockCode(code="1234", name="test_user", position=1)
        ]
        params = smart_lock.DeleteKeyCodeParams(username="test_user")

        # Act
        result = self.sut.delete_key_code(params)

        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Key code deleted")
        self.assertIn(1, self.fake_position_deleter.deleted_positions)

    def test_delete_key_code_not_found(self):
        # Arrange
        self.fake_code_lister.codes = [
            smart_lock.LockCode(code="5678", name="another_user", position=1)
        ]
        params = smart_lock.DeleteKeyCodeParams(username="test_user")

        # Act
        result = self.sut.delete_key_code(params)

        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Key code not found")
        self.assertNotIn(1, self.fake_position_deleter.deleted_positions)

    def test_list_key_codes(self):
        # Arrange
        self.fake_code_lister.codes = [
            smart_lock.LockCode(code="1234", name="user1", position=1),
            smart_lock.LockCode(code="5678", name="user2", position=2),
        ]

        # Act
        result = self.sut.list_key_codes()

        # Assert
        self.assertEqual(len(result.codes), 2)
        self.assertEqual(result.codes[0].code, "1234")
        self.assertEqual(result.codes[1].code, "5678")

    def test_create_key_code_maximum_codes(self):
        # Arrange
        self.fake_code_lister.codes = [smart_lock.LockCode(code=str(i), name=f"user{i}", position=i) for i in range(1, 251)]
        params = smart_lock.CreateKeyCodeParams(code="9999", username="new_user")

        # Act / Assert
        with self.assertRaises(ValueError) as context:
            self.sut.create_key_code(params)
        self.assertEqual(str(context.exception), "Maximum number of codes reached")

    def test_get_next_position(self):
        # Arrange
        self.fake_code_setter.next_position = 5

        # Act
        result = self.sut.get_next_position()

        # Assert
        self.assertEqual(result, 5)

    @patch('time.time')
    def test_create_key_code_timestamp(self, mock_time):
        # Arrange
        mock_time.return_value = 1630000000
        params = smart_lock.CreateKeyCodeParams(code="1234", username="test_user")

        # Act
        result = self.sut.create_key_code(params)

        # Assert
        self.assertEqual(result.timestamp, 1630000000)

class TestWebdriverBasedComponents(TestCase):
    @patch('hubitat_lock_manager.smart_lock.webdriver.Chrome')
    def test_webdriver_based_code_deleter(self, mock_chrome):
        # Arrange
        config = smart_lock.WebdriverConfig(hub_ip="192.168.1.100", command_executor="")
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_form = Mock()
        mock_driver.find_element.return_value = mock_form
        
        deleter = smart_lock.create_webdriver_based_code_deleter(device_id=1, config=config)

        # Act
        deleter.delete_position(smart_lock.DeletePositionParams(position=1))

        # Assert
        mock_driver.get.assert_called_once_with("http://192.168.1.100/device/edit/1")
        mock_driver.find_element.assert_called_once()
        mock_form.find_element.assert_called_once()
        mock_form.submit.assert_called_once()
        mock_driver.quit.assert_called_once()

    @patch('hubitat_lock_manager.smart_lock.webdriver.Chrome')
    def test_webdriver_based_code_lister(self, mock_chrome):
        # Arrange
        config = smart_lock.WebdriverConfig(hub_ip="192.168.1.100", command_executor="")
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_element = Mock()
        mock_element.get_attribute.return_value = '{"1": {"code": "1234", "name": "user1"}}'
        mock_driver.find_element.return_value = mock_element
        
        lister = smart_lock.create_webdriver_based_code_lister(config)

        # Act
        result = lister.list_codes(device_id=1)

        # Assert
        self.assertIsInstance(result, smart_lock.ListKeyCodesResult)
        self.assertEqual(len(result.codes), 1)
        self.assertEqual(result.codes[0].code, "1234")
        self.assertEqual(result.codes[0].name, "user1")
        self.assertEqual(result.codes[0].position, 1)
        mock_driver.get.assert_called_once_with("http://192.168.1.100/device/edit/1")
        mock_driver.quit.assert_called_once()

    @patch('hubitat_lock_manager.smart_lock.webdriver.Chrome')
    def test_webdriver_based_code_setter(self, mock_chrome):
        # Arrange
        config = smart_lock.WebdriverConfig(hub_ip="192.168.1.100", command_executor="")
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_form = Mock()
        mock_driver.find_element.return_value = mock_form
        
        setter = smart_lock.create_webdriver_based_code_setter(device_id=1, config=config)

        # Act
        result = setter.set_code(smart_lock.SetCodeParams(code="5678", name="newuser"))

        # Assert
        self.assertIsInstance(result, smart_lock.SetCodeResult)
        mock_driver.get.assert_called_once_with("http://192.168.1.100/device/edit/1")
        mock_driver.find_element.assert_called_once()
        self.assertEqual(mock_form.find_element.call_count, 3)  # Three input fields
        mock_form.submit.assert_called_once()
        mock_driver.quit.assert_called_once()

class TestHelperFunctions(TestCase):
    def test_get_next_position_based_on_list_key_codes_result(self):
        # Arrange
        codes = [
            smart_lock.LockCode(code="1111", name="user1", position=1),
            smart_lock.LockCode(code="2222", name="user2", position=2),
            smart_lock.LockCode(code="3333", name="user3", position=4)
        ]
        result = smart_lock.ListKeyCodesResult(codes=codes)

        # Act
        next_position = smart_lock.get_next_position_based_on_list_key_codes_result(result)

        # Assert
        self.assertEqual(next_position, 3)

    def test_get_next_position_all_positions_filled(self):
        # Arrange
        codes = [smart_lock.LockCode(code=str(i), name=f"user{i}", position=i) for i in range(1, 251)]
        result = smart_lock.ListKeyCodesResult(codes=codes)

        # Act
        next_position = smart_lock.get_next_position_based_on_list_key_codes_result(result)

        # Assert
        self.assertEqual(next_position, 250)  # Should return the last possible position

if __name__ == "__main__":
    unittest.main()
