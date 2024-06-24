from dataclasses import dataclass

from selenium import webdriver

from hubitat_lock_manager.factory import SmartLockFactory
from hubitat_lock_manager.hubitat_manager import HubitatManager
from hubitat_lock_manager.models import CreateKeyCodeParams, UpdateKeyCodeParams, DeleteKeyCodeParams

@dataclass(frozen=True)
class SmartLockController:
    factory: SmartLockFactory
    driver_path: str = "path/to/chromedriver"

    def create_key_code(self, params: CreateKeyCodeParams):
        driver = webdriver.Chrome(executable_path=self.driver_path)
        smart_lock = self.factory.create_smart_lock(driver)
        with HubitatManager(driver=driver, smart_lock=smart_lock) as manager:
            result = manager.create_key_code(params)
        return result

    def update_key_code(self, params: UpdateKeyCodeParams):
        driver = webdriver.Chrome(executable_path=self.driver_path)
        smart_lock = self.factory.create_smart_lock(driver)
        with HubitatManager(driver=driver, smart_lock=smart_lock) as manager:
            result = manager.update_key_code(params)
        return result

    def delete_key_code(self, params: DeleteKeyCodeParams):
        driver = webdriver.Chrome(executable_path=self.driver_path)
        smart_lock = self.factory.create_smart_lock(driver)
        with HubitatManager(driver=driver, smart_lock=smart_lock) as manager:
            result = manager.delete_key_code(params)
        return result

    def list_key_codes(self):
        driver = webdriver.Chrome(executable_path=self.driver_path)
        smart_lock = self.factory.create_smart_lock(driver)
        with HubitatManager(driver=driver, smart_lock=smart_lock) as manager:
            result = manager.list_key_codes()
        return result
