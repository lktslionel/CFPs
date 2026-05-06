"""
Services
"""

from typing import Optional

from returns.maybe import Some
from returns.result import Failure, Result
from shared.metadata import Metadata

from domain.errors import DomainError
from domain.models import Certificate, CertificateStatus
from domain.repositories import (
    CertificateNotFoundError,
    CertificateRepository,
    RepositoryQueryFilter,
)
from domain.types import DomainName


class CertificateRenewalService:
    """ """

    _provider: CertificateRepository
    """Certificate source of trust where the renewed certificate is located. 
    Eg: Sectigo Certificate Manager"""

    _consumer: CertificateRepository
    """Certificate store target where the certificate will be re-imported. 
    Eg: AWS ACM"""

    def __init__(
        self, *, provider: CertificateRepository, consumer: CertificateRepository
    ) -> None:
        self._provider = provider
        self._consumer = consumer

    def renew_certificate(
        self, *, common_name: DomainName, extras: Optional[Metadata] = None
    ) -> Result[Certificate, DomainError]:
        """
        Get a valid (issued) certificate for the given domain name, from the origin certificate provider,
        and replace the expiring certificate for the same domain name within thethe consumer's certiifcate store
        with the valid one.

        Parameters:
            common_name (DomainName): Domain name for which the certificate is expiring

        Returns:
            Either the issued certificate or the domain error that occured during the process
        """

        issued: Certificate
        expiring: Certificate

        # 1. Get expiring certificicate from the certificate consumer
        match self._consumer.find_by_name(common_name):
            case Some(certificate):
                expiring = certificate
            case _:
                return Failure(
                    CertificateNotFoundError(
                        source=self._consumer.source,
                        common_name=common_name,
                    )
                )

        # 2. Get a valid certificicate from the certificate provider
        issued_certificate_filter = RepositoryQueryFilter(
            status=CertificateStatus.ISSUED
        )

        match self._provider.find_by_name(
            common_name, query_filter=issued_certificate_filter
        ):
            case Some(certificate):
                issued = certificate
            case _:
                return Failure(
                    CertificateNotFoundError(
                        source=self._provider.source,
                        common_name=common_name,
                        query_filter=issued_certificate_filter,
                    )
                )

        # 3. Update expiring certificate data with the issued certificate data
        expiring.data = issued.data

        # 4. Update certificate tags on consumer repository to match
        #    the issued certificate id from the provider repository
        expiring.tag("saws.security:cert-mgt.cro/sectigo.certmanager.id", issued.id)

        # 5. Re-import the expiring certificate with its data renewed
        return self._consumer.save(expiring)
