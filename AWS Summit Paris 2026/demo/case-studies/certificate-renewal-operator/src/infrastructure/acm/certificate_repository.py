from __future__ import annotations

from typing import Iterator, Optional

from domain.errors import DomainError
from domain.models import Certificate, CertificateMetadata
from domain.repositories import (
    CertificateRepositorySource,
    RepositoryQueryFilter,
)
from domain.types import DomainName
from more_itertools import flatten, map_except
from mypy_boto3_acm.client import ACMClient
from mypy_boto3_acm.type_defs import CertificateSummaryTypeDef
from pydantic import ValidationError
from returns.result import Result
from shared.constants import DEFAULT_DATETIME_FORMAT

from infrastructure.errors import InfrastructureError


class AcmCertificateRepository:
    source: CertificateRepositorySource = CertificateRepositorySource.AWS_ACM
    _session: ACMClient

    def __init__(self, session: ACMClient) -> None:
        self._session = session

    def find(
        self,
        *,
        query_filter: Optional[RepositoryQueryFilter] = None,
    ) -> Iterator[Certificate]:
        request = {}

        if query_filter:
            request["CertificateStatuses"] = (
                [query_filter.status] if query_filter.status else []
            )

        paginator = self._session.get_paginator("list_certificates")

        certificate_summary_list = flatten(
            [page["CertificateSummaryList"] for page in paginator.paginate(**request)]
        )

        # Collect certificates except those which raise a validation error
        certificates = map_except(
            self.create_certificate_from_summary_response,
            certificate_summary_list,
            ValidationError,
        )

        return certificates

    def find_by_id(
        self,
        id: str,
        *,
        include_tags: Optional[bool] = False,
        query_filter: Optional[RepositoryQueryFilter] = None,
    ) -> Optional[Certificate]:
        certificate_found = next(
            filter(
                lambda certificate: certificate.id == id,
                self.find(
                    query_filter=query_filter,
                ),
            ),
            None,
        )

        return certificate_found

    def find_by_name(
        self,
        common_name: DomainName,
        *,
        include_tags: Optional[bool] = False,
        query_filter: Optional[RepositoryQueryFilter] = None,
    ) -> Optional[Certificate]:
        certificate_found = next(
            filter(
                lambda certificate: certificate.common_name == common_name,
                self.find(
                    query_filter=query_filter,
                ),
            ),
            None,
        )

        return certificate_found

    def save(
        self, certificate: Certificate
    ) -> Result[
        Certificate,
        DomainError | InfrastructureError,
    ]:
        ...

    def delete(
        self, certificate: Certificate
    ) -> Result[
        Certificate,
        DomainError | InfrastructureError,
    ]:
        ...

    @classmethod
    def create_certificate_from_summary_response(
        cls: type[AcmCertificateRepository],
        summary: CertificateSummaryTypeDef,
    ) -> Certificate:
        _certificate = Certificate.model_validate(
            {
                "id": summary.get("CertificateArn"),
                "common_name": summary.get("DomainName"),
                "status": summary.get("Status"),
                "metadata": CertificateMetadata(provider="aws.acm"),
            }
        )

        created_at = summary.get("CreatedAt")
        if created_at:
            _certificate.tag(
                "saws.security:cert-mgt.cro/acm.created_at",
                created_at.strftime(DEFAULT_DATETIME_FORMAT),
            )

        imported_at = summary.get("ImportedAt")
        if imported_at:
            _certificate.tag(
                "saws.security:cert-mgt.cro/acm.imported_at",
                imported_at.strftime(DEFAULT_DATETIME_FORMAT),
            )

        return _certificate
