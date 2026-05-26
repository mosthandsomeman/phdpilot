"""PostgreSQL enum helpers — persist enum .value (e.g. 'user'), not .name (e.g. 'USER')."""

import enum
from typing import TypeVar

from sqlalchemy import Enum as SAEnum

E = TypeVar("E", bound=enum.Enum)


def pg_enum(enum_cls: type[E], *, name: str | None = None, **kwargs) -> SAEnum:
    return SAEnum(
        enum_cls,
        name=name or enum_cls.__name__.lower(),
        values_callable=lambda members: [m.value for m in members],
        native_enum=False,
        **kwargs,
    )
