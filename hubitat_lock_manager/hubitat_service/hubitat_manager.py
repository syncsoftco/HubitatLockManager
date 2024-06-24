from dataclasses import dataclass
from selenium.webdriver.remote.webdriver import WebDriver
from .smart_lock import SmartLock, CreateKeyCodeParams, CreateKeyCodeResult, UpdateKeyCodeParams, UpdateKeyCodeResult, DeleteKeyCodeParams, DeleteKeyCodeResult, ReadKeyCodeParams, ReadKeyCodeResult, ListKeyCodesResult

@dataclass(frozen=True)
class HubitatManager:
    driver: WebDriver
    smart_lock: SmartLock

    def login(self, url, username):
        self.driver.get(url)
        self.driver.find_element_by_id('username').send_keys(username)
        self.driver.find_element_by_id('loginButton').click()

    def create_key_code(self, params: CreateKeyCodeParams) -> CreateKeyCodeResult:
        return self.smart_lock.create_key_code(params)

    def update_key_code(self, params: UpdateKeyCodeParams) -> UpdateKeyCodeResult:
        return self.smart_lock.update_key_code(params)

    def delete_key_code(self, params: DeleteKeyCodeParams) -> DeleteKeyCodeResult:
        return self.smart_lock.delete_key_code(params)

    def read_key_code(self, params: ReadKeyCodeParams) -> ReadKeyCodeResult:
        return self.smart_lock.read_key_code(params)

    def list_key_codes(self) -> ListKeyCodesResult:
        return self.smart_lock.list_key_codes()

    def close(self):
        self.driver.quit()
