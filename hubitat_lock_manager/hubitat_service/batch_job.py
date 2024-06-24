import time
from dataclasses import dataclass
from .hubitat_manager import HubitatManager
from .factory import create_yale_assure_lever
from distributed.queue_manager import QueueManager
from distributed.datastore import DataStore
from selenium import webdriver

@dataclass(frozen=True)
class BatchJob:
    manager: HubitatManager
    queue: QueueManager
    datastore: DataStore

    def run(self):
        while True:
            tasks = self.queue.get_tasks()
            for task in tasks:
                # Process each task based on the task type
                pass
            time.sleep(60)

    def stop(self):
        self.manager.close()

# Function to initialize BatchJob with dependencies
def init_batch_job(driver_path, hubitat_url, username):
    driver = webdriver.Chrome(executable_path=driver_path)
    smart_lock = create_yale_assure_lever(driver)
    manager = HubitatManager(driver, smart_lock)
    manager.login(hubitat_url, username)
    queue = QueueManager()
    datastore = DataStore()
    return BatchJob(manager, queue, datastore)
