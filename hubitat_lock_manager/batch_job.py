from dataclasses import dataclass
from selenium import webdriver
from hubitat_lock_manager.hubitat_manager import HubitatManager
from hubitat_lock_manager.smart_lock import create_yale_assure_lever
from hubitat_lock_manager.datastore import DataStore
import hashlib

@dataclass(frozen=True)
class BatchJob:
    manager: HubitatManager
    data_store: DataStore

def init_batch_job(driver_path: str, hubitat_url: str, username: str, password: str, db_connection) -> BatchJob:
    driver = webdriver.Chrome(executable_path=driver_path)
    smart_lock = create_yale_assure_lever(driver)
    manager = HubitatManager(driver=driver, smart_lock=smart_lock)
    data_store = DataStore(connection=db_connection)
    manager.login(url=hubitat_url, username=username, password=password)
    return BatchJob(manager=manager, data_store=data_store)

def hash_request(timestamp: float, code: str, name: str) -> str:
    return hashlib.sha256(f"{timestamp}-{code}-{name}".encode()).hexdigest()

def run_batch_job(batch_job: BatchJob):
    pending_codes = batch_job.data_store.get_pending_key_codes()
    pending_codes.sort(key=lambda x: x["timestamp"])  # Ensure requests are processed in order

    for code_request in pending_codes:
        lock_id = code_request["lock_id"]
        code = code_request["code"]
        name = code_request["name"]
        request_timestamp = code_request["timestamp"]
        request_hash = hash_request(request_timestamp, code, name)

        if not batch_job.data_store.is_request_processed(request_hash):
            result = batch_job.manager.create_key_code(CreateKeyCodeParams(lock_id=lock_id, code=code, name=name))
            batch_job.data_store.record_key_code_result(lock_id, code, name, result.success, result.message, request_hash)
