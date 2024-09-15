import json
import time
from dataclasses import dataclass
from typing import Callable, Iterable

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@dataclass(frozen=True)
class CodeLister:
    list_codes: Callable[[int], "ListKeyCodesResult"]


@dataclass(frozen=True)
class CodeSetter:
    get_next_position: Callable[[], int]
    set_code: Callable[["SetCodeParams"], "SetCodeResult"]


@dataclass(frozen=True)
class CreateKeyCodeParams:
    code: str
    username: str


@dataclass(frozen=True)
class CreateKeyCodeResult:
    position: int
    timestamp: int


@dataclass(frozen=True)
class CreateSmartLockParams:
    device_id: int
    config: "SmartLockConfig"


@dataclass(frozen=True)
class DeleteKeyCodeParams:
    username: str


@dataclass(frozen=True)
class DeleteKeyCodeResult:
    success: bool
    message: str


@dataclass(frozen=True)
class DeletePositionParams:
    position: int


@dataclass(frozen=True)
class Device:
    id: int
    name: str


@dataclass(frozen=True)
class Factory:
    create_smart_lock: Callable[[CreateSmartLockParams], "SmartLock"]
    list_smart_locks: Callable[[], "ListDevicesResult"]


@dataclass(frozen=True)
class ListDevicesResult:
    devices: Iterable[Device]


@dataclass(frozen=True)
class ListKeyCodesResult:
    codes: Iterable["LockCode"]


@dataclass(frozen=True)
class LockCode:
    code: str
    name: str
    position: int


@dataclass(frozen=True)
class DeviceLister:
    list_devices: Callable[[], ListDevicesResult]


@dataclass(frozen=True)
class PositionDeleter:
    delete_position: Callable[["DeletePositionParams"], None]


@dataclass(frozen=True)
class SetCodeParams:
    code: str
    name: str


@dataclass(frozen=True)
class SetCodeResult:
    position: int


@dataclass(frozen=True)
class SmartLock:
    create_key_code: Callable[[CreateKeyCodeParams], CreateKeyCodeResult]
    delete_key_code: Callable[[DeleteKeyCodeParams], DeleteKeyCodeResult]
    get_next_position: Callable[[], int]
    list_key_codes: Callable[[], ListKeyCodesResult]


@dataclass(frozen=True)
class SmartLockConfig:
    device_lister: DeviceLister
    smart_lock_factory: Factory


@dataclass(frozen=True)
class WebdriverConfig:
    hub_ip: str
    device_name_filter: str = "lock"

    @staticmethod
    def create_driver() -> webdriver.Chrome:
        options = webdriver.ChromeOptions()    # ChromeDriver can be sensitive to version changes, so we use these arguments to improve stability
        options.add_argument("start-maximized")  # Start the browser maximized
        options.add_argument("enable-automation")  # Enable automation mode
        options.add_argument("--headless")  # Run in headless mode (no GUI)
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("--disable-browser-side-navigation")  # Avoid errors on page load timeout
        options.add_argument("--disable-gpu")  # Applicable to windows os only
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )


def create_generic_z_wave_lock(
    device_id: int,
    position_deleter: PositionDeleter,
    code_lister: CodeLister,
    code_setter: CodeSetter,
) -> SmartLock:
    def create_key_code(params: CreateKeyCodeParams) -> CreateKeyCodeResult:
        existing_codes = code_lister.list_codes(device_id).codes
        if any(lock_code.code == params.code for lock_code in existing_codes):
            raise ValueError(f"Code {params.code} already exists")

        if any(lock_code.name == params.username for lock_code in existing_codes):
            raise ValueError(f"Key code for {params.username} already exists")

        timestamp = int(time.time())
        set_code_result = code_setter.set_code(
            SetCodeParams(params.code, params.username)
        )
        return CreateKeyCodeResult(set_code_result.position, timestamp=timestamp)

    def delete_key_code(
        params: DeleteKeyCodeParams,
    ) -> DeleteKeyCodeResult:
        existing_codes = code_lister.list_codes(device_id).codes
        position = next(
            (
                lock_code.position
                for lock_code in existing_codes
                if lock_code.name == params.username
            ),
            None,
        )
        if not position:
            return DeleteKeyCodeResult(success=True, message="Key code not found")

        params = DeletePositionParams(position=position)
        position_deleter.delete_position(params)
        return DeleteKeyCodeResult(success=True, message="Key code deleted")

    def list_key_codes() -> ListKeyCodesResult:
        return code_lister.list_codes(device_id)

    return SmartLock(
        create_key_code=create_key_code,
        delete_key_code=delete_key_code,
        get_next_position=code_setter.get_next_position,
        list_key_codes=list_key_codes,
    )


def create_webdriver_based_code_deleter(
    device_id: int, config: WebdriverConfig
) -> PositionDeleter:
    def delete_position(params: DeletePositionParams) -> None:
        driver = config.create_driver()
        try:
            # Navigate to the device edit page
            driver.get(f"http://{config.hub_ip}/device/edit/{device_id}")

            # Locate the form element by its id
            form = driver.find_element(By.ID, "form-deleteCode-1")

            # Now locate the child input field within this form
            code_position = form.find_element(By.NAME, "arg[1]")

            # Fill in the field
            code_position.send_keys(
                str(params.position)
            )  # Replace with the desired code position

            # Submit the form
            form.submit()
        finally:
            driver.quit()

    return PositionDeleter(delete_position)


def create_webdriver_based_code_lister(config: WebdriverConfig) -> CodeLister:
    def list_codes(device_id: int) -> ListKeyCodesResult:
        return get_codes_via_webdriver(device_id, config)

    return CodeLister(list_codes)


def create_webdriver_based_code_setter(
    device_id: int, config: WebdriverConfig
) -> CodeSetter:
    def get_next_position() -> int:
        return get_next_position_via_webdriver(device_id, config)

    def set_code(params: SetCodeParams) -> SetCodeResult:
        driver = config.create_driver()
        try:
            # Navigate to the device edit page
            driver.get(f"http://{config.hub_ip}/device/edit/{device_id}")

            # Locate the form element by its id
            form = driver.find_element(By.ID, "form-setCode-5")

            # Now locate the child input fields within this form
            code_position = form.find_element(By.NAME, "arg[1]")
            pin_code = form.find_element(By.NAME, "arg[2]")
            name = form.find_element(By.NAME, "arg[3]")

            position = get_next_position()

            print(f"Setting code at position {position}")

            # Fill in the fields
            code_position.send_keys(
                str(position)
            )  # Replace with the desired code position
            pin_code.send_keys(str(params.code))  # Replace with the desired PIN code
            name.send_keys(params.name)  # Replace with the desired name

            # Submit the form
            form.submit()

            # Wait for the page to reload
            time.sleep(5)

            return SetCodeResult(position=position)
        finally:
            driver.quit()

    return CodeSetter(get_next_position, set_code)


def create_webdriver_device_lister(config: WebdriverConfig) -> DeviceLister:
    def list_devices() -> ListDevicesResult:
        return list_devices_via_webdriver(config)

    return DeviceLister(list_devices)


def create_webdriver_smart_lock_config(config: WebdriverConfig) -> SmartLockConfig:
    device_lister = create_webdriver_device_lister(config)
    smart_lock_factory = create_webdriver_smart_lock_factory(config)
    return SmartLockConfig(device_lister, smart_lock_factory)


def create_webdriver_smart_lock_factory(config: WebdriverConfig) -> Factory:
    def create_smart_lock(params: CreateSmartLockParams) -> SmartLock:
        position_deleter = create_webdriver_based_code_deleter(params.device_id, config)
        code_lister = create_webdriver_based_code_lister(config)
        code_setter = create_webdriver_based_code_setter(params.device_id, config)

        return create_generic_z_wave_lock(
            params.device_id, position_deleter, code_lister, code_setter
        )

    def list_smart_locks() -> ListDevicesResult:
        list_devices_result = list_devices_via_webdriver(config)

        # Filter out devices that are not locks
        devices = filter(
            lambda d: config.device_name_filter in d.name.lower(),
            list_devices_result.devices,
        )

        return ListDevicesResult(devices=list(devices))

    return Factory(create_smart_lock, list_smart_locks)


def get_codes_via_webdriver(
    device_id: int, config: WebdriverConfig
) -> ListKeyCodesResult:
    driver = config.create_driver()
    try:
        url = f"http://{config.hub_ip}/device/edit/{device_id}"

        driver.get(url)

        # Locate the element containing the JSON-like string
        element = driver.find_element(By.ID, "cstate-value-lockCodes")

        # Extract the text from the element
        json_text = element.get_attribute("innerText").strip()

        # Parse the JSON-like string into a Python dictionary
        lock_codes_dict = json.loads(json_text)

        # Convert the dictionary into a list of dictionaries
        lock_codes_list = [
            {"position": int(key), "code": value["code"], "name": value["name"]}
            for key, value in lock_codes_dict.items()
        ]

        return ListKeyCodesResult(
            codes=[LockCode(**lock_code) for lock_code in lock_codes_list]
        )
    finally:
        driver.quit()


def get_next_position_based_on_list_key_codes_result(result: ListKeyCodesResult) -> int:
    existing_positions = frozenset(lock_code.position for lock_code in result.codes)
    return next(p for p in range(250, 0, -1) if p not in existing_positions)


def list_devices_via_webdriver(config: WebdriverConfig) -> ListDevicesResult:
    driver = config.create_driver()
    try:
        # Navigate to the devices page
        driver.get(f"http://{config.hub_ip}/device/list")

        # Locate the table element containing the devices
        table = driver.find_element(By.ID, "device-table")

        # Locate the rows within the table's body
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        # Extract the device information from each row
        devices = []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")

            # Skip rows without cells (e.g., header or empty rows)
            if not cells:
                continue

            # Adjust the cell indices based on the actual table structure
            # Assuming the device ID and name are in the 1st and 2nd cell respectively
            device_id = row.get_attribute("data-device-id")
            device_name = cells[1].text

            devices.append(Device(id=int(device_id), name=device_name))

        return ListDevicesResult(devices=devices)
    finally:
        driver.quit()


def get_next_position_via_webdriver(device_id: int, config: WebdriverConfig) -> int:
    result = get_codes_via_webdriver(device_id, config)
    return get_next_position_based_on_list_key_codes_result(result)
