"""
Infrastructure Errors
"""
from enum import IntEnum, auto
from functools import partial
from typing import Optional

from shared.errors import Error, ErrorScope


class InfrastructureErrorIds(IntEnum):
    DEFAULT = auto()
    CERTIFICATE_REPOSITORY_VALUE_ERROR = auto()


class InfrastructureError(Error):
    def __init__(
        self,
        id: int,
        reason: Optional[str] = None,
        origin: Optional[Exception] = None,
    ):
        super().__init__(
            id=id,
            scope=ErrorScope.INFRASTRUCTURE,
            reason=reason,
            origin=origin,
        )


DefaultError = partial(
    InfrastructureError,
    id=InfrastructureErrorIds.DEFAULT,
)

CertificateRepositoryValueError = partial(
    InfrastructureError,
    id=InfrastructureErrorIds.CERTIFICATE_REPOSITORY_VALUE_ERROR,
)
