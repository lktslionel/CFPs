"""
Errors
"""

from dataclasses import dataclass
from enum import Enum, auto, unique
from typing import Optional


@unique
class ErrorScope(Enum):
    UNKOWN = auto()
    UI = auto()
    APPLICATION = auto()
    DOMAIN = auto()
    INFRASTRUCTURE = auto()


@dataclass
class Error(Exception):
    """
    Base Error class for others classes to extend


    Attributes
    ----------
    id : int
        Error identifier unique within the scope & category
    scope : ErrorScope
        Error scope
            1: ui
            2: application
            3: domain
            4: infrastructure
    reason: Optional[str]
        Error message
    origin: Optional[Exception]
        Error which causes this error to occure
    """

    id: int
    scope: ErrorScope

    reason: Optional[str] = None
    origin: Optional[Exception] = None

    def __post_init__(self):
        self.code = f"ERR-{self.scope.value}-{self.id}"

    def __str__(self) -> str:
        message = self.reason or self.__class__.__name__
        return f"{self.code}: {message}"
