"""
Repositories Interfaces
"""

from enum import StrEnum, unique
from typing import Iterator, NamedTuple, Optional, Protocol, runtime_checkable

from infrastructure.errors import InfrastructureError
from returns.maybe import Maybe
from returns.result import Result

from domain.errors import DomainError, DomainErrorIds
from domain.models import Certificate, CertificateStatus
from domain.types import DomainName


@unique
class CertificateRepositorySource(StrEnum):
    AWS_ACM = "aws.acm"
    SCM = "scm"


class RepositoryQueryFilter(NamedTuple):
    status: Optional[CertificateStatus] = None


class CertificateNotFoundError(DomainError):
    id: DomainErrorIds = DomainErrorIds.CERTIFICATE_NOT_FOUND

    def __init__(
        self,
        *,
        source: CertificateRepositorySource,
        common_name: DomainName,
        query_filter: Optional[RepositoryQueryFilter] = None,
    ) -> None:
        message = f"""Certificate not found when quering repository source[{source}] \
with common name[{common_name}] and filter[{query_filter}]
"""
        super().__init__(
            id=self.id,
            reason=message,
        )


@runtime_checkable
class CertificateRepository(Protocol):
    """Contract to satisfy to be a repository"""

    # repository source name to identify and distinguish the repository from each other
    source: CertificateRepositorySource

    def find(
        self,
        *,
        query_filter: Optional[RepositoryQueryFilter] = None,
    ) -> Iterator[Certificate]:
        ...

    def find_by_id(
        self,
        id: str,
        *,
        include_tags: Optional[bool] = False,
        query_filter: Optional[RepositoryQueryFilter] = None,
    ) -> Optional[Certificate]:
        ...

    def find_by_name(
        self,
        common_name: DomainName,
        *,
        include_tags: Optional[bool] = False,
        query_filter: Optional[RepositoryQueryFilter] = None,
    ) -> Optional[Certificate]:
        ...

    def save(
        self, certificate: Certificate
    ) -> Result[Certificate, DomainError | InfrastructureError]:
        """
        Return either the saved certificate if successful or the domain error if any failure occur

        Parameters:
            certificate (Certificate): Certificate to save

        Returns:
            Either Success(certificate) or Failure(DomainError)
        """
        ...

    def delete(
        self, certificate: Certificate
    ) -> Result[Certificate, DomainError | DomainError | InfrastructureError]:
        """
        Return either the deleted certificate if successful or the domain error if any failure occur

        Parameters:
            certificate (Certificate): Certificate to delete

        Returns:
            Either Success(certificate) or Failure(DomainError)
        """
        ...
