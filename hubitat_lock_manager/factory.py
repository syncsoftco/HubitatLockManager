from enum import Enum
import functools

from selenium.webdriver.remote.webdriver import WebDriver
from hubitat_lock_manager.smart_lock import create_yale_assure_lever
from hubitat_lock_manager.models import SmartLock

class SmartLockFactory(Enum):
    TEST_FACTORY = functools.partial(lambda driver: SmartLock())
    YALE_ASSURE_LEVER = functools.partial(create_yale_assure_lever)

    def create_smart_lock(self, driver: WebDriver) -> SmartLock:
        return self.value(driver)
