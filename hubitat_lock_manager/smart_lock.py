from selenium.webdriver.remote.webdriver import WebDriver
from hubitat_lock_manager.models import (
    CreateKeyCodeParams,
    CreateKeyCodeResult,
    UpdateKeyCodeParams,
    UpdateKeyCodeResult,
    DeleteKeyCodeParams,
    DeleteKeyCodeResult,
    ListKeyCodesResult,
    SmartLock,
)

from hubitat_lock_manager.models import (
    CreateKeyCodeParams,
    CreateKeyCodeResult,
    UpdateKeyCodeParams,
    UpdateKeyCodeResult,
    DeleteKeyCodeParams,
    DeleteKeyCodeResult,
    ListKeyCodesResult,
    SmartLock,
)


def create_test_lock(driver: WebDriver) -> SmartLock:
    def create_key_code(params: CreateKeyCodeParams) -> CreateKeyCodeResult:
        return CreateKeyCodeResult(success=True, message="Stubbed: Key code created")

    def update_key_code(params: UpdateKeyCodeParams) -> UpdateKeyCodeResult:
        return UpdateKeyCodeResult(success=True, message="Stubbed: Key code updated")

    def delete_key_code(params: DeleteKeyCodeParams) -> DeleteKeyCodeResult:
        return DeleteKeyCodeResult(success=True, message="Stubbed: Key code deleted")

    def list_key_codes() -> ListKeyCodesResult:
        codes = [CreateKeyCodeParams(code="1234", name="Test Code")]
        return ListKeyCodesResult(codes=codes)

    return SmartLock(
        create_key_code=create_key_code,
        update_key_code=update_key_code,
        delete_key_code=delete_key_code,
        list_key_codes=list_key_codes,
    )


def create_yale_assure_lever(driver: WebDriver) -> SmartLock:
    def create_key_code(params: CreateKeyCodeParams) -> CreateKeyCodeResult:
        # Selenium logic for creating key code
        return CreateKeyCodeResult(success=True, message="Key code created")

    def update_key_code(params: UpdateKeyCodeParams) -> UpdateKeyCodeResult:
        # Selenium logic for updating key code
        return UpdateKeyCodeResult(success=True, message="Key code updated")

    def delete_key_code(params: DeleteKeyCodeParams) -> DeleteKeyCodeResult:
        # Selenium logic for deleting key code
        return DeleteKeyCodeResult(success=True, message="Key code deleted")

    def list_key_codes() -> ListKeyCodesResult:
        # Selenium logic for listing key codes
        codes = [CreateKeyCodeParams(code="1234", name="Test Code")]
        return ListKeyCodesResult(codes=codes)

    return SmartLock(
        create_key_code=create_key_code,
        update_key_code=update_key_code,
        delete_key_code=delete_key_code,
        list_key_codes=list_key_codes,
    )
