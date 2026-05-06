"""
Domain Errors
"""
from enum import IntEnum, auto
from functools import partial
from typing import Optional

from shared import errors
from shared.errors import ErrorScope


class DomainErrorIds(IntEnum):
    DEFAULT = auto()
    CERTIFICATE_NOT_FOUND = auto()


class DomainError(errors.Error):
    def __init__(
        self,
        id: int,
        reason: Optional[str] = None,
        origin: Optional[Exception] = None,
    ):
        super().__init__(
            id=id,
            scope=ErrorScope.DOMAIN,
            reason=reason,
            origin=origin,
        )


DefaultError = partial(
    DomainError,
    id=DomainErrorIds.DEFAULT,
)
