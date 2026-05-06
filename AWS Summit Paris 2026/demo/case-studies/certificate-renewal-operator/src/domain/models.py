"""
Certificate Models
"""

import uuid
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional, Set

from pydantic import BaseModel

from domain.types import (
    AllowedCertificateTagKeys,
    CertificatePoviderStr,
    DomainName,
    KeyValuePairs,
)


class CertificateStatus(StrEnum):
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
    INACTIVE = "INACTIVE"
    ISSUED = "ISSUED"
    PENDING_VALIDATION = "PENDING_VALIDATION"
    REVOKED = "REVOKED"
    VALIDATION_TIMED_OUT = "VALIDATION_TIMED_OUT"


@dataclass
class CertificateMetadata:
    provider: CertificatePoviderStr


@dataclass
class CertificateData:
    """
    Contains the certificate, private key and the chain of trust certificates
    as the PEM-encoded text
    """

    certificate: str
    private_key: str
    certificate_chain: Optional[Set[str]]


class Certificate(BaseModel):
    """
    Certifcate
    """

    id: str
    common_name: DomainName
    status: Optional[CertificateStatus] = None
    data: Optional[CertificateData] = None
    metadata: Optional[CertificateMetadata] = None
    tags: KeyValuePairs = {}

    def has_data(self):
        return self.data is not None

    def tag(self, key: AllowedCertificateTagKeys, value: str) -> bool:
        """Apply a tag on the certificate and update the value of the tag if its key already exist"""

        self.tags.update({key: value})
        return self.tags.get(key, None) == value

    @classmethod
    def of_common_name(
        cls,
        name: DomainName,
        *,
        id: str = str(uuid.uuid4()),
        status: Optional[CertificateStatus] = None,
        data: Optional[CertificateData] = None,
        metadata: Optional[CertificateMetadata] = None,
        tags: KeyValuePairs = {},
    ):
        return cls(
            id=id,
            common_name=name,
            status=status,
            data=data,
            metadata=metadata,
            tags=tags,
        )
