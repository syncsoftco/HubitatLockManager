from selenium import webdriver
from .smart_lock import SmartLock

class HubitatManager:
    def __init__(self, driver_path, smart_lock: SmartLock):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.smart_lock = smart_lock

    def login(self, url, username, password):
        self.driver.get(url)
        self.driver.find_element_by_id('username').send_keys(username)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('loginButton').click()

    def create_key_code(self, params):
        return self.smart_lock.create_key_code(params)

    def update_key_code(self, params):
        return self.smart_lock.update_key_code(params)

    def delete_key_code(self, params):
        return self.smart_lock.delete_key_code(params)

    def read_key_code(self, params):
        return self.smart_lock.read_key_code(params)

    def close(self):
        self.driver.quit()
