from __future__ import annotations

import warnings
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Dict

from pydantic.utils import update_not_none
from pydantic.validators import decimal_validator

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class SecretDecimal:
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        update_not_none(field_schema, type="Decimal", writeOnly=True, format="password")

    @classmethod
    def __get_validators__(cls) -> CallableGenerator:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> SecretDecimal:
        if isinstance(value, cls):
            return value
        value = decimal_validator(value)
        return cls(value)

    def __init__(self, value: Decimal):
        self._secret_value = value

    def __repr__(self) -> str:
        return f"SecretDecimal('{self}')"

    def __str__(self) -> str:
        return "**********" if self._secret_value else ""

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, SecretDecimal)
            and self.get_secret_value() == other.get_secret_value()
        )

    def display(self) -> str:
        warnings.warn(
            "`pydantic_secret_decimal.display()` is deprecated, use `str(secret_decimal)` instead",
            DeprecationWarning,
        )
        return str(self)

    def get_secret_value(self) -> Decimal:
        return self._secret_value
