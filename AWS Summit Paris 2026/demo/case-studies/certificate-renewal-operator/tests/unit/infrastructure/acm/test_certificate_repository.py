import datetime
import random
import re
from unittest import mock
from xml.etree.ElementInclude import include

import pytest
from domain.models import Certificate, CertificateStatus
from domain.repositories import RepositoryQueryFilter
from infrastructure import acm
from infrastructure.acm.certificate_repository import AcmCertificateRepository
from infrastructure.errors import InfrastructureError, InfrastructureErrorIds
from more_itertools import ilen
from mypy_boto3_acm.client import ACMClient
from mypy_boto3_acm.paginator import (
    ListCertificatesPaginator,
)
from returns.methods import unwrap_or_failure
from returns.result import Failure
from shared.constants import DEFAULT_DATETIME_FORMAT

from .fakes import fake_domain_name


def test_create_repository_instance(dummy_acm_session: ACMClient):
    repository = acm.AcmCertificateRepository(session=dummy_acm_session)

    assert repository is not None


class TestFindCertificates:
    def test_with_no_filter(
        self,
        repository: AcmCertificateRepository,
        fake_acm_list_certificates_respones,
        monkeypatch,
    ):
        fake_paginator = mock.MagicMock(spec=ListCertificatesPaginator)
        fake_paginator.paginate.return_value = fake_acm_list_certificates_respones

        monkeypatch.setattr(
            repository._session,
            "get_paginator",
            lambda operation_name: fake_paginator,
        )

        # with mock.patch.object(dummy_acm_session, "get_paginator") as fake_paginator:
        #     fake_paginator.paginate.return_value = fake_acm_list_certificates_respones

        certificates_found = repository.find()

        assert ilen(certificates_found) > 0

    def test_with_id(
        self,
        repository: AcmCertificateRepository,
        fake_acm_list_certificates_respones,
        monkeypatch,
    ):
        fake_paginator = mock.MagicMock(spec=ListCertificatesPaginator)
        fake_paginator.paginate.return_value = fake_acm_list_certificates_respones

        monkeypatch.setattr(
            repository._session,
            "get_paginator",
            lambda operation_name: fake_paginator,
        )

        expected_response = random.choice(fake_acm_list_certificates_respones)
        expected_summary = random.choice(
            expected_response.get("CertificateSummaryList")
        )
        requested_id = expected_summary.get("CertificateArn")

        certificate_found = repository.find_by_id(requested_id)

        assert certificate_found is not None

    def test_with_id_and_tags_included(
        self,
        repository: AcmCertificateRepository,
        fake_acm_list_certificates_respones,
        monkeypatch,
    ):
        fake_paginator = mock.MagicMock(spec=ListCertificatesPaginator)
        fake_paginator.paginate.return_value = fake_acm_list_certificates_respones

        monkeypatch.setattr(
            repository._session,
            "get_paginator",
            lambda operation_name: fake_paginator,
        )

        expected_response = random.choice(fake_acm_list_certificates_respones)
        expected_summary = random.choice(
            expected_response.get("CertificateSummaryList")
        )
        requested_id = expected_summary.get("CertificateArn")

        certificate = repository.find_by_id(
            requested_id,
            include_tags=True,
        )

        assert certificate is not None

    def test_with_name(
        self,
        repository: AcmCertificateRepository,
        fake_acm_list_certificates_respones,
        monkeypatch,
    ):
        fake_paginator = mock.MagicMock(spec=ListCertificatesPaginator)
        fake_paginator.paginate.return_value = fake_acm_list_certificates_respones

        monkeypatch.setattr(
            repository._session,
            "get_paginator",
            lambda operation_name: fake_paginator,
        )

        expected_response = random.choice(fake_acm_list_certificates_respones)
        expected_summary = random.choice(
            expected_response.get("CertificateSummaryList")
        )
        requested_common_name = expected_summary.get("DomainName")

        certificate_found = repository.find_by_name(requested_common_name)

        assert certificate_found is not None


class TestSavingCertificate:
    def test_save_certificate_without_data(
        self,
        repository: AcmCertificateRepository,
    ):
        certificate = Certificate.of_common_name(
            fake_domain_name(),
            status=CertificateStatus.ISSUED,
        )

        result = unwrap_or_failure(
            repository.save(certificate),
        )

        assert isinstance(result, InfrastructureError)
        assert result.id == InfrastructureErrorIds.CERTIFICATE_REPOSITORY_VALUE_ERROR
        assert result.reason is not None
        assert "missing certificate data" in result.reason

    def test_save_certificate_without_tags(
        self,
        repository: AcmCertificateRepository,
    ):
        certificate = Certificate.of_common_name(
            fake_domain_name(),
            status=CertificateStatus.ISSUED,
        )

        result = unwrap_or_failure(
            repository.save(certificate),
        )

        assert isinstance(result, InfrastructureError)
        assert result.id == InfrastructureErrorIds.CERTIFICATE_REPOSITORY_VALUE_ERROR
        assert result.reason is not None
        assert "missing certificate data" in result.reason
