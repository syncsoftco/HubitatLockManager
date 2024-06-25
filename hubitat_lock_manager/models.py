from dataclasses import dataclass, field
from typing import List, Callable


@dataclass(frozen=True)
class CreateKeyCodeParams:
    code: str
    name: str


@dataclass(frozen=True)
class CreateKeyCodeResult:
    success: bool
    message: str


@dataclass(frozen=True)
class UpdateKeyCodeParams:
    old_code: str
    new_code: str
    new_name: str


@dataclass(frozen=True)
class UpdateKeyCodeResult:
    success: bool
    message: str


@dataclass(frozen=True)
class DeleteKeyCodeParams:
    code: str


@dataclass(frozen=True)
class DeleteKeyCodeResult:
    success: bool
    message: str


@dataclass(frozen=True)
class ListKeyCodesResult:
    codes: List[CreateKeyCodeParams]


@dataclass(frozen=True)
class SmartLock:
    create_key_code: Callable[[CreateKeyCodeParams], CreateKeyCodeResult]
    update_key_code: Callable[[UpdateKeyCodeParams], UpdateKeyCodeResult]
    delete_key_code: Callable[[DeleteKeyCodeParams], DeleteKeyCodeResult]
    list_key_codes: Callable[[], ListKeyCodesResult]
