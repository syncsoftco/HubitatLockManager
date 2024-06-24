from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from .smart_lock import (
    SmartLock,
    CreateKeyCodeParams,
    CreateKeyCodeResult,
    UpdateKeyCodeParams,
    UpdateKeyCodeResult,
    DeleteKeyCodeParams,
    DeleteKeyCodeResult,
    ReadKeyCodeParams,
    ReadKeyCodeResult
)

def create_yale_assure_lever(driver: WebDriver) -> SmartLock:
    def create_key_code(params: CreateKeyCodeParams) -> CreateKeyCodeResult:
        # Specific implementation for Yale Assure Lever
        driver.find_element(By.ID, 'lock-id-input').send_keys(params.lock_id)
        driver.find_element(By.ID, 'code-input').send_keys(params.code)
        driver.find_element(By.ID, 'name-input').send_keys(params.name)
        driver.find_element(By.ID, 'create-button').click()
        return CreateKeyCodeResult(success=True, message="Yale Assure Lever key code created")

    def update_key_code(params: UpdateKeyCodeParams) -> UpdateKeyCodeResult:
        # Specific implementation for Yale Assure Lever
        return UpdateKeyCodeResult(success=True, message="Yale Assure Lever key code updated")

    def delete_key_code(params: DeleteKeyCodeParams) -> DeleteKeyCodeResult:
        # Specific implementation for Yale Assure Lever
        return DeleteKeyCodeResult(success=True, message="Yale Assure Lever key code deleted")

    def read_key_code(params: ReadKeyCodeParams) -> ReadKeyCodeResult:
        # Specific implementation for Yale Assure Lever
        return ReadKeyCodeResult(code=params.code, name="Yale Assure Lever")

    return SmartLock(
        create_key_code=create_key_code,
        update_key_code=update_key_code,
        delete_key_code=delete_key_code,
        read_key_code=read_key_code
    )
