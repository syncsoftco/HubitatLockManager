from dataclasses import dataclass

from hubitat_lock_manager.hubitat_manager import HubitatManager
from hubitat_lock_manager.models import CreateKeyCodeParams, UpdateKeyCodeParams, DeleteKeyCodeParams
from selenium import webdriver
from hubitat_lock_manager.factory import SmartLockFactory

@dataclass(frozen=True)
class SmartLockController:
    def __init__(self):
        self.driver_path = "path/to/chromedriver"

    def create_key_code(self, params: CreateKeyCodeParams):
        driver = webdriver.Chrome(executable_path=self.driver_path)
        smart_lock = SmartLockFactory.create_smart_lock(SmartLockFactory.YALE_ASSURE_LEVER, driver)
        with HubitatManager(driver=driver, smart_lock=smart_lock, lock_id=LOCK_ID) as manager:
            result = manager.create_key_code(params)
        return result

    def update_key_code(self, params: UpdateKeyCodeParams):
        driver = webdriver.Chrome(executable_path=self.driver_path)
        smart_lock = SmartLockFactory.create_smart_lock(SmartLockFactory.YALE_ASSURE_LEVER, driver)
        with HubitatManager(driver=driver, smart_lock=smart_lock, lock_id=LOCK_ID) as manager:
            result = manager.update_key_code(params)
        return result

    def delete_key_code(self, params: DeleteKeyCodeParams):
        driver = webdriver.Chrome(executable_path=self.driver_path)
        smart_lock = SmartLockFactory.create_smart_lock(SmartLockFactory.YALE_ASSURE_LEVER, driver)
        with HubitatManager(driver=driver, smart_lock=smart_lock, lock_id=LOCK_ID) as manager:
            result = manager.delete_key_code(params)
        return result

    def list_key_codes(self):
        driver = webdriver.Chrome(executable_path=self.driver_path)
        smart_lock = SmartLockFactory.create_smart_lock(SmartLockFactory.YALE_ASSURE_LEVER, driver)
        with HubitatManager(driver=driver, smart_lock=smart_lock, lock_id=LOCK_ID) as manager:
            result = manager.list_key_codes()
        return result
