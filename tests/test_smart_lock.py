import os
import unittest

from hubitat_lock_manager import smart_lock

DEVICE_IDS = os.getenv("DEVICE_IDS", "1,2,3").split(",")
HUB_IP = os.getenv("HUB_IP", "hub_ip")
LOCK_CODE = os.getenv("LOCK_CODE", "54337082")
NAME = os.getenv("NAME", "Shane McCauley")

print(f"Lock code under test: {LOCK_CODE}")


class WebdriverSmartLockFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.device_ids = [int(device_id) for device_id in DEVICE_IDS]
        self.config = smart_lock.WebdriverConfig(HUB_IP)
        self.factory = smart_lock.create_webdriver_smart_lock_factory(self.config)
        self.webdriver_config = smart_lock.WebdriverConfig(HUB_IP)
        self.smart_lock_config = smart_lock.create_webdriver_smart_lock_config(
            self.webdriver_config
        )

    def test_create_smart_lock(self):
        for device_id in self.device_ids:
            with self.subTest(device_id=device_id):
                # Arrange
                params = smart_lock.CreateSmartLockParams(
                    device_id, self.smart_lock_config
                )

                # Act
                actual = self.factory.create_smart_lock(params)

                # Assert
                self.assertIsInstance(actual, smart_lock.SmartLock)


class WebdriverSmartLockCreateKeyCodeTestCase(unittest.TestCase):
    def setUp(self):
        webdriver_config = smart_lock.WebdriverConfig(HUB_IP)

        self.device_ids = [int(device_id) for device_id in DEVICE_IDS]
        self.factory = smart_lock.create_webdriver_smart_lock_factory(webdriver_config)
        self.smart_lock_config = smart_lock.create_webdriver_smart_lock_config(
            webdriver_config
        )
        self.create_key_code_params = smart_lock.CreateKeyCodeParams(LOCK_CODE, NAME)

    def test_create_key_code(self):
        for device_id in self.device_ids:
            with self.subTest(device_id=device_id):
                # Arrange
                create_smart_lock_params = smart_lock.CreateSmartLockParams(
                    device_id, self.smart_lock_config
                )
                sut = self.factory.create_smart_lock(create_smart_lock_params)
                expected_position = sut.get_next_position()
                expected_code = smart_lock.LockCode(LOCK_CODE, NAME, expected_position)

                # Act
                sut.create_key_code(self.create_key_code_params)

                # Assert
                self.assertIn(expected_code, sut.list_key_codes().codes)


if __name__ == "__main__":
    unittest.main()
