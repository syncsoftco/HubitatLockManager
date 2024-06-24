import time
from .hubitat_manager import HubitatManager
from .factory import create_yale_assure_lever
from distributed.queue_manager import QueueManager
from distributed.datastore import DataStore

class BatchJob:
    def __init__(self, driver_path, hubitat_url, username, password):
        smart_lock = create_yale_assure_lever(driver_path)
        self.manager = HubitatManager(driver_path, smart_lock)
        self.manager.login(hubitat_url, username, password)
        self.queue = QueueManager()
        self.datastore = DataStore()

    def run(self):
        while True:
            tasks = self.queue.get_tasks()
            for task in tasks:
                # Process each task based on the task type
                pass
            time.sleep(60)

    def stop(self):
        self.manager.close()
