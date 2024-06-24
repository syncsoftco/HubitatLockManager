from selenium.webdriver.remote.webdriver import WebDriver
from hubitat_lock_manager.models import CreateKeyCodeParams, UpdateKeyCodeParams, DeleteKeyCodeParams, SmartLock

@dataclass(frozen=True)
class HubitatManager:
    driver: WebDriver
    smart_lock: SmartLock

    def login(self):
        # Selenium logic for logging into Hubitat
        pass

    def create_key_code(self, params: CreateKeyCodeParams):
        return self.smart_lock.create_key_code(params)

    def update_key_code(self, params: UpdateKeyCodeParams):
        return self.smart_lock.update_key_code(params)

    def delete_key_code(self, params: DeleteKeyCodeParams):
        return self.smart_lock.delete_key_code(params)

    def list_key_codes(self):
        return self.smart_lock.list_key_codes()

    def close(self):
        self.driver.quit()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
