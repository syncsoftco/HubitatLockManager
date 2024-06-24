from dataclasses import dataclass, field
from typing import List, Callable

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
    code_id: str
    new_code: str
    new_name: str

@dataclass(frozen=True)
class UpdateKeyCodeResult:
    success: bool
    message: str

@dataclass(frozen=True)
class DeleteKeyCodeParams:
    lock_id: str
    code_id: str

@dataclass(frozen=True)
class DeleteKeyCodeResult:
    success: bool
    message: str

@dataclass(frozen=True)
class ReadKeyCodeParams:
    lock_id: str
    code_id: str

@dataclass(frozen=True)
class ReadKeyCodeResult:
    code: str
    name: str

@dataclass(frozen=True)
class ListKeyCodesResult:
    codes: List[ReadKeyCodeResult]

@dataclass(frozen=True)
class SmartLock:
    create_key_code: Callable[[CreateKeyCodeParams], CreateKeyCodeResult]
    update_key_code: Callable[[UpdateKeyCodeParams], UpdateKeyCodeResult]
    delete_key_code: Callable[[DeleteKeyCodeParams], DeleteKeyCodeResult]
    read_key_code: Callable[[ReadKeyCodeParams], ReadKeyCodeResult]
    list_key_codes: Callable[[str], ListKeyCodesResult]
