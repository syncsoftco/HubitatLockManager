import unittest
from unittest import TestCase
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

        self.sut = create_generic_z_wave_lock(
            self.device_id, self.fake_position_deleter, self.fake_code_lister, self.fake_code_setter
        )

    def test_create_key_code_success(self):
        # Arrange
        params = CreateKeyCodeParams(code="1234", username="test_user")

        # Act
        result = self.sut.create_key_code(params)

        # Assert
        self.assertEqual(result.position, 1)
        self.assertGreater(result.timestamp, 0)
        self.assertIn("1234", [code.code for code in self.fake_code_setter.codes])

    def test_create_key_code_duplicate_code(self):
        # Arrange
        self.fake_code_lister.codes = [
            LockCode(code="1234", name="user1", position=1)
        ]
        params = smart_lock.CreateKeyCodeParams(code="1234", username="test_user")

        # Act / Assert
        with self.assertRaises(ValueError) as context:
            self.sut.create_key_code(params)
        self.assertEqual(str(context.exception), "Code 1234 already exists")

    def test_create_key_code_duplicate_username(self):
        # Arrange
        self.fake_code_lister.codes = [
            LockCode(code="5678", name="test_user", position=1)
        ]
        params = CreateKeyCodeParams(code="1234", username="test_user")

        # Act / Assert
        with self.assertRaises(ValueError) as context:
            self.sut.create_key_code(params)
        self.assertEqual(str(context.exception), "Key code for test_user already exists")

    def test_delete_key_code_success(self):
        # Arrange
        self.fake_code_lister.codes = [
            LockCode(code="1234", name="test_user", position=1)
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
            LockCode(code="5678", name="another_user", position=1)
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
            smart_lock.LockCode(code="5678", name="user2", position=2)
        ]

        # Act
        result = self.sut.list_key_codes()

        # Assert
        self.assertEqual(len(result.codes), 2)
        self.assertEqual(result.codes[0].code, "1234")
        self.assertEqual(result.codes[1].code, "5678")


if __name__ == "__main__":
    unittest.main()
