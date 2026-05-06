from collections import defaultdict
from contextlib import suppress
from typing import List, Optional

from domain.errors import DomainError
from domain.models import Certificate
from domain.repositories import (
    CertificateNotFoundError,
    CertificateRepository,
    CertificateRepositorySource,
    RepositoryQueryFilter,
)
from domain.types import DomainName
from returns.maybe import Maybe, Nothing, Some
from returns.result import Failure, Result, Success


class FakeCertificateRepository(CertificateRepository):
    source: CertificateRepositorySource

    def __init__(
        self, source: CertificateRepositorySource, seed: List[Certificate]
    ) -> None:
        self.source = source
        self.values_by_names = defaultdict(None)
        self.values_by_ids = defaultdict(None)

        for certificate in seed:
            self.values_by_names[certificate.common_name] = certificate
            self.values_by_ids[certificate.id] = certificate

    def find_by_id(
        self, id: str, query_filter: Optional[RepositoryQueryFilter] = None
    ) -> Maybe[Certificate]:
        value = self.values_by_ids.get(id)
        return Some(value) if value else Nothing

    def find_by_name(
        self,
        common_name: DomainName,
        query_filter: Optional[RepositoryQueryFilter] = None,
    ) -> Maybe[Certificate]:
        value = self.values_by_names.get(common_name)

        return Some(value) if value else Nothing

    def save(self, certificate: Certificate) -> Result[Certificate, DomainError]:
        self.values_by_names[certificate.common_name] = certificate
        self.values_by_ids[certificate.id] = certificate

        return Success(certificate)

    def delete(self, certificate: Certificate) -> Result[Certificate, DomainError]:
        with suppress(KeyError):
            del self.values_by_names[certificate.common_name]
            del self.values_by_ids[certificate.id]

            return Success(certificate)

        return Failure(
            CertificateNotFoundError(
                source=self.source, common_name=certificate.common_name
            )
        )
