from typing import Optional

from domain.errors import DomainError
from domain.models import Certificate
from domain.repositories import (
    CertificateRepositorySource,
    RepositoryQueryFilter,
)
from domain.types import DomainName
from returns.maybe import Maybe, Nothing, Some
from returns.result import Failure, Result, Success


class ScmCertificateRepository:
    source: CertificateRepositorySource = CertificateRepositorySource.SCM

    def __init__(self) -> None:
        pass

    def find_by_id(
        self, id: str, query_filter: Optional[RepositoryQueryFilter] = None
    ) -> Maybe[Certificate]:
        return Nothing

    def find_by_name(
        self,
        common_name: DomainName,
        query_filter: Optional[RepositoryQueryFilter] = None,
    ) -> Maybe[Certificate]:
        return Nothing

    def save(self, certificate: Certificate) -> Result[Certificate, DomainError]:
        return Nothing

    def delete(self, certificate: Certificate) -> Result[Certificate, DomainError]:
        return Nothing
