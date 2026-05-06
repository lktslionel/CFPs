from unittest import mock

import pytest
from domain.models import CertificateStatus
from infrastructure import acm
from infrastructure.acm.certificate_repository import AcmCertificateRepository
from mypy_boto3_acm.client import ACMClient

from .fakes import generate_acm_list_certificates_responses


@pytest.fixture
def fake_acm_list_certificates_respones():
    return list(
        generate_acm_list_certificates_responses(
            count=10,
            status=CertificateStatus.ISSUED,
            acm_type="IMPORTED",
        )
    )


@pytest.fixture()
def dummy_acm_session() -> ACMClient:
    _acm = mock.MagicMock(spec=ACMClient)
    return _acm  # type: ignore


@pytest.fixture
def repository(dummy_acm_session: ACMClient) -> AcmCertificateRepository:
    return acm.AcmCertificateRepository(session=dummy_acm_session)
