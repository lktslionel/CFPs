from dataclasses import dataclass
from typing import NamedTuple, Self

from domain.repositories import CertificateRepository
from domain.services import CertificateRenewalService
from domain.types import DomainName
from infrastructure.acm import AcmCertificateRepository
from infrastructure.scm import ScmCertificateRepository
from returns.result import Failure, Success
from shared.metadata import Metadata

from application.certificate_renewal.events.certificate_approaching_expiration import (
    CertificateApproachingExpirationEvent,
)

from ..command import AbstractCommand


@dataclass(kw_only=True)
class RenewCertificateCommand(AbstractCommand):
    """Execute a certificate renewal request"""

    # Act as a request id to trace the transaction
    id: str
    expiring_domain_name: DomainName

    @classmethod
    def from_event(cls, event: CertificateApproachingExpirationEvent) -> Self:
        return cls(id=event.id, expiring_domain_name=event.detail.common_name)

    def execute(self):
        acm: CertificateRepository = AcmCertificateRepository()
        scm: CertificateRepository = ScmCertificateRepository()

        service: CertificateRenewalService = CertificateRenewalService(
            provider=scm, consumer=acm
        )

        # We inject the request/command id as metadata for tracing purposes
        metadata: Metadata = {"correlation-id": self.id}
        match service.renew_certificate(
            common_name=self.expiring_domain_name, extras=metadata
        ):
            case Success(renewed):
                pass
            case Failure(error):
                pass
