import pytest
from domain.models import (
    Certificate,
    CertificateData,
    CertificateMetadata,
    CertificateStatus,
)
from domain.repositories import (
    CertificateNotFoundError,
    CertificateRepository,
    CertificateRepositorySource,
)
from domain.services import CertificateRenewalService
from domain.types import DomainName
from returns.result import Failure, Success

from tests.utilities import pki
from tests.utilities.mock import FakeCertificateRepository


@pytest.fixture
def valid_issued_id():
    return "1111"


@pytest.fixture
def scm_repository(valid_issued_id):
    [certificate, private_key] = pki.generate_selfsigned_cert(hostname="*.example.com")

    fakes = [
        Certificate.of_common_name(
            "*.example.com",
            id=valid_issued_id,
            status=CertificateStatus.ISSUED,
            metadata=CertificateMetadata(provider="sectigo.certmanager"),
            data=CertificateData(
                certificate=certificate.hex(),
                private_key=private_key.hex(),
                certificate_chain=None,
            ),
        ),
        Certificate.of_common_name(
            "test.example.com",
            id="2222",
            status=CertificateStatus.EXPIRED,
            metadata=CertificateMetadata(provider="sectigo.certmanager"),
        ),
    ]

    return FakeCertificateRepository(source=CertificateRepositorySource.SCM, seed=fakes)


@pytest.fixture
def acm_repository():
    [certificate, private_key] = pki.generate_selfsigned_cert(hostname="*.example.com")

    fakes = [
        Certificate.of_common_name(
            "*.example.com",
            id="arn:aws:acm:eu-central-1:x:certificate/61f50cd4-45b9-4259-b049-d0a53682fa4b",
            status=CertificateStatus.ISSUED,
            metadata=CertificateMetadata(provider="aws.acm"),
            data=CertificateData(
                certificate=certificate.hex(),
                private_key=private_key.hex(),
                certificate_chain=None,
            ),
            tags={
                "saws.security:cert-mgt.cro/sectigo.certmanager.id": "0000",
            },
        ),
        Certificate.of_common_name(
            "svc-a.example.com",
            id="arn:aws:acm:eu-central-1:x:certificate/a58fbd30-3e56-4300-a55e-09722998d272",
            status=CertificateStatus.ISSUED,
            metadata=CertificateMetadata(provider="aws.acm"),
        ),
    ]

    return FakeCertificateRepository(
        source=CertificateRepositorySource.AWS_ACM, seed=fakes
    )


class TestCertificateRenewalService:
    def test_fixtures_repositories_can_act_as_certificate_repositories(
        self, acm_repository, scm_repository
    ):
        assert isinstance(acm_repository, CertificateRepository)
        assert isinstance(scm_repository, CertificateRepository)

    def test_renew_expiring_certificate_on_acm_with_scm_issued_certificate(
        self,
        valid_issued_id,
        acm_repository: CertificateRepository,
        scm_repository: CertificateRepository,
    ):
        domain_name: DomainName = "*.example.com"

        service = CertificateRenewalService(
            provider=scm_repository, consumer=acm_repository
        )

        match service.renew_certificate(common_name=domain_name):
            case Success(issued):
                assert (
                    issued.tags.get("saws.security:cert-mgt.cro/sectigo.certmanager.id")
                    == valid_issued_id
                )
            case _:
                raise Exception(f"Failed to renew certificate for domain{domain_name}")

    def test_renew_expiring_certificate_present_in_acm_and_missing_in_scm(
        self,
        valid_issued_id,
        acm_repository: CertificateRepository,
        scm_repository: CertificateRepository,
    ):
        domain_name: DomainName = "svc-a.example.com"

        service = CertificateRenewalService(
            provider=scm_repository, consumer=acm_repository
        )

        match service.renew_certificate(common_name=domain_name):
            case Failure(error):
                assert isinstance(error, CertificateNotFoundError)

                assert domain_name in str(error)
                assert CertificateRepositorySource.SCM.value in str(error)
            case _:
                raise Exception(
                    f"Failed to renew certificate for domain[{domain_name}]"
                )

    def test_renew_expiring_certificate_present_in_scm_and_missing_in_acm(
        self,
        valid_issued_id,
        acm_repository: CertificateRepository,
        scm_repository: CertificateRepository,
    ):
        domain_name: DomainName = "test.example.com"

        service = CertificateRenewalService(
            provider=scm_repository, consumer=acm_repository
        )

        match service.renew_certificate(common_name=domain_name):
            case Failure(error):
                assert isinstance(error, CertificateNotFoundError)

                assert domain_name in str(error)
                assert CertificateRepositorySource.AWS_ACM.value in str(error)
            case _:
                raise Exception(
                    f"Failed to renew certificate for domain[{domain_name}]"
                )

    def test_renew_expiring_certificate_missing_in_both_scm_and_acm(
        self,
        valid_issued_id,
        acm_repository: CertificateRepository,
        scm_repository: CertificateRepository,
    ):
        domain_name: DomainName = "missing.example.com"

        service = CertificateRenewalService(
            provider=scm_repository, consumer=acm_repository
        )

        match service.renew_certificate(common_name=domain_name):
            case Failure(error):
                assert isinstance(error, CertificateNotFoundError)
                assert domain_name in str(error)
            case _:
                raise Exception(
                    f"Failed to renew certificate for domain[{domain_name}]"
                )
