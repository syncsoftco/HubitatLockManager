import dataclasses
from enum import Enum
from typing import Iterable, Optional

from hubitat_lock_manager import smart_lock


class WebdriverBasedSmartLockFactories(Enum):
    GENERIC_Z_WAVE_LOCK = smart_lock.Factory(
        lambda params: smart_lock.create_generic_z_wave_lock(
            code_lister=smart_lock.create_webdriver_based_code_lister(
                params.config.webdriver_config
            ),
            code_setter=smart_lock.create_webdriver_based_code_setter(
                params.device_id, params.config.webdriver_config
            ),
            position_deleter=smart_lock.create_webdriver_based_code_deleter(
                params.device_id, params.config.webdriver_config
            ),
            device_id=params.device_id,
        ),
        lambda params: smart_lock.list_devices_via_webdriver(
            params.config.webdriver_config
        ),
    )

    def create_smart_lock(
        self, params: smart_lock.CreateSmartLockParams
    ) -> smart_lock.SmartLock:
        return self.value.create_smart_lock(params)


@dataclasses.dataclass(frozen=True)
class SmartLockController:
    lock_provider: "SmartLockProvider"

    def create_key_code(
        self, username: str, code: str, device_id: int
    ) -> smart_lock.CreateKeyCodeResult:
        # Ensure code is 8 digits and numeric
        if not code.isdigit() or len(code) != 8:
            raise ValueError("Code must be 8 digits and numeric")

        existing_key_code = self.get_key_code(username, device_id, code)
        if not existing_key_code:
            params = smart_lock.CreateKeyCodeParams(code=code, username=username)
            device = self.lock_provider.get_smart_lock(device_id)
            return device.create_key_code(params)

        if existing_key_code.code != code:
            raise ValueError(f"Key code for {username} already exists")

        raise ValueError(f"Code {code} already exists for {username}")

    def create_key_code_on_all_devices(
        self, username: str, code: str
    ) -> Iterable[smart_lock.CreateKeyCodeResult]:
        result = self.list_devices()
        for device in result.devices:
            yield self.create_key_code(username, code, device["id"])

    def delete_key_code(
        self, username: str, device_id: int
    ) -> smart_lock.DeleteKeyCodeResult:
        device = self.lock_provider.get_smart_lock(device_id)
        params = smart_lock.DeleteKeyCodeParams(username)
        return device.delete_key_code(params)

    def delete_key_code_on_all_devices(
        self, username: str
    ) -> Iterable[smart_lock.DeleteKeyCodeResult]:
        result = self.list_devices()
        for device in result.devices:
            yield self.delete_key_code(username, device["id"])

    def get_key_code(
        self, username: str, device_id: int, code: str = ""
    ) -> Optional[smart_lock.LockCode]:
        return next(
            (
                lock_code
                for lock_code in self.list_key_codes(device_id).codes
                if lock_code.name == username or lock_code.code == code
            ),
            None,
        )

    def list_devices(self) -> smart_lock.ListDevicesResult:
        return self.lock_provider.list_smart_locks()

    def list_key_codes(self, device_id: int) -> smart_lock.ListKeyCodesResult:
        return self.lock_provider.get_smart_lock(device_id).list_key_codes()

    def update_key_code(self, device_id: int, username: str, code: str):
        self.delete_key_code(username, device_id)
        self.create_key_code(username, code, device_id)


@dataclasses.dataclass(frozen=True)
class SmartLockControllerFactory:
    smart_lock_factory: smart_lock.Factory

    def create_smart_lock_controller(
        self, config: smart_lock.SmartLockConfig
    ) -> SmartLockController:
        provider = SmartLockProvider(self.smart_lock_factory, config)
        return SmartLockController(provider)


@dataclasses.dataclass(frozen=True)
class SmartLockProvider:
    smart_lock_factory: smart_lock.Factory
    smart_lock_config: smart_lock.SmartLockConfig

    def get_smart_lock(self, device_id: int):
        device_id = int(device_id)
        create_smart_lock_params = smart_lock.CreateSmartLockParams(
            device_id, self.smart_lock_config
        )
        return self.smart_lock_factory.create_smart_lock(create_smart_lock_params)

    def list_smart_locks(self):
        return self.smart_lock_factory.list_smart_locks()


def create_smart_lock_controller(
    config: smart_lock.SmartLockConfig,
) -> SmartLockController:
    smart_lock_factory = config.smart_lock_factory()
    smart_lock_controller_factory = SmartLockControllerFactory(smart_lock_factory)
    return smart_lock_controller_factory.create_smart_lock_controller(config)


def create_webdriver_based_smart_lock_factory(
    smart_lock_config: smart_lock.SmartLockConfig,
) -> smart_lock.Factory:
    def create_smart_lock(
        params: smart_lock.CreateSmartLockParams,
    ) -> smart_lock.SmartLock:
        factory = WebdriverBasedSmartLockFactories.GENERIC_Z_WAVE_LOCK.value
        return factory.create_smart_lock(
            smart_lock.CreateSmartLockParams(params.device_id, smart_lock_config)
        )

    def list_smart_locks() -> smart_lock.ListDevicesResult:
        return smart_lock.list_devices_via_webdriver(smart_lock_config.webdriver)

    return smart_lock.Factory(create_smart_lock, list_smart_locks)
