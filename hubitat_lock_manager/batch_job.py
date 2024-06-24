from dataclasses import dataclass
from selenium import webdriver
from hubitat_lock_manager.hubitat_manager import HubitatManager
from hubitat_lock_manager.smart_lock import create_yale_assure_lever

@dataclass(frozen=True)
class BatchJob:
    manager: HubitatManager

def init_batch_job(driver_path: str, hubitat_url: str, username: str, password: str) -> BatchJob:
    driver = webdriver.Chrome(executable_path=driver_path)
    smart_lock = create_yale_assure_lever(driver)
    manager = HubitatManager(driver=driver, smart_lock=smart_lock)
    manager.login(url=hubitat_url, username=username, password=password)
    return BatchJob(manager=manager)
