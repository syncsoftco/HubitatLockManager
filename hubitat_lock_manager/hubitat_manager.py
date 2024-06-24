from dataclasses import dataclass

from selenium.webdriver.remote.webdriver import WebDriver
from hubitat_lock_manager.models import CreateKeyCodeParams, UpdateKeyCodeParams, DeleteKeyCodeParams, ReadKeyCodeParams, SmartLock

@dataclass(frozen=True)
class HubitatManager:
    driver: WebDriver
    smart_lock: SmartLock

    def login(self, url: str, username: str, password: str):
        # Selenium logic for logging into Hubitat
        pass

    def create_key_code(self, params: CreateKeyCodeParams):
        return self.smart_lock.create_key_code(params)

    def update_key_code(self, params: UpdateKeyCodeParams):
        return self.smart_lock.update_key_code(params)

    def delete_key_code(self, params: DeleteKeyCodeParams):
        return self.smart_lock.delete_key_code(params)

    def read_key_code(self, params: ReadKeyCodeParams):
        return self.smart_lock.read_key_code(params)

    def list_key_codes(self, lock_id: str):
        return self.smart_lock.list_key_codes(lock_id)

    def close(self):
        self.driver.quit()
