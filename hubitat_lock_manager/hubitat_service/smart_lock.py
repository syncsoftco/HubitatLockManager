from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class CreateKeyCodeParams:
    lock_id: str
    code: str
    name: str

@dataclass(frozen=True)
class CreateKeyCodeResult:
    success: bool
    message: str

@dataclass(frozen=True)
class UpdateKeyCodeParams:
    lock_id: str
    code: str
    new_code: str
    new_name: str

@dataclass(frozen=True)
class UpdateKeyCodeResult:
    success: bool
    message: str

@dataclass(frozen=True)
class DeleteKeyCodeParams:
    lock_id: str
    code: str

@dataclass(frozen=True)
class DeleteKeyCodeResult:
    success: bool
    message: str

@dataclass(frozen=True)
class ReadKeyCodeParams:
    lock_id: str
    code: str

@dataclass(frozen=True)
class ReadKeyCodeResult:
    code: str
    name: str

@dataclass
class SmartLock:
    create_key_code: Callable[[CreateKeyCodeParams], CreateKeyCodeResult]
    update_key_code: Callable[[UpdateKeyCodeParams], UpdateKeyCodeResult]
    delete_key_code: Callable[[DeleteKeyCodeParams], DeleteKeyCodeResult]
    read_key_code: Callable[[ReadKeyCodeParams], ReadKeyCodeResult]
