import dataclasses
from typing import Iterable, Optional

from hubitat_lock_manager import smart_lock


@dataclasses.dataclass(frozen=True)
class CreateKeyCodeParams:
    code: str
    username: str
    device_id: int = -1

    @property
    def has_device_id(self):
        return self.device_id > -1


@dataclasses.dataclass(frozen=True)
class SmartLockController:
    lock_provider: "SmartLockProvider"

    def create_key_code(
        self, params: CreateKeyCodeParams
    ) -> Iterable[smart_lock.CreateKeyCodeResult]:
        """
        Create a key code for a user on one or more smart lock devices.
        :param params: The parameters for creating the key code.
        :return: An iterable of the results of creating the key code.
        """
        if params.has_device_id:
            yield self.create_key_code_on_one_device(
                params.username, params.code, params.device_id
            )
            return

        yield from self.create_key_code_on_all_devices(params.username, params.code)

    def create_key_code_on_one_device(
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
            yield self.create_key_code_on_one_device(username, code, device.id)

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
            yield self.delete_key_code(username, device.id)

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
        self.create_key_code_on_one_device(username, code, device_id)


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


def create_smart_lock_controller(hub_ip: str, command_executor: str) -> SmartLockController:
    # Configure how the code will interact with the Hubitat web interface
    webdriver_config = smart_lock.WebdriverConfig(hub_ip, command_executor)

    # Create a more specific configuration tailored for using a web browser
    config = smart_lock.create_webdriver_smart_lock_config(webdriver_config)

    smart_lock_controller_factory = SmartLockControllerFactory(
        config.smart_lock_factory
    )
    return smart_lock_controller_factory.create_smart_lock_controller(config)
