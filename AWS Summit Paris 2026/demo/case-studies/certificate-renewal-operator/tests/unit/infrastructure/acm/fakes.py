import random
from typing import Any, Generator, Literal, Mapping, Optional, get_args

from domain.models import CertificateStatus
from faker import Faker
from faker.providers import internet, misc, python
from infrastructure.acm.types import ACMCertificateTypes
from shared.constants import DEFAULT_DATETIME_FORMAT

_fake = Faker()
Faker.seed(0)
_fake.add_provider(internet)
_fake.add_provider(python)
_fake.add_provider(misc)


_DEFAULT_RESPONSES_COUNT = 5


def generate_acm_list_certificates_responses(
    *,
    status: Optional[CertificateStatus] = None,
    acm_type: Optional[ACMCertificateTypes] = None,
    count: int = _DEFAULT_RESPONSES_COUNT,
) -> Generator[Mapping[str, Any], None, None]:
    subject_alternative_names = [
        _fake.domain_name(level)
        for level in range(
            1,
            _fake.pyint(
                2,
                3,
            ),
        )
    ]

    return (
        {
            "NextToken": _fake.uuid4(),
            "CertificateSummaryList": [
                {
                    "CertificateArn": f"arn:aws:acm:region:account:certificate/{_fake.uuid4()}",
                    "DomainName": _fake.domain_name(),
                    "SubjectAlternativeNameSummaries": subject_alternative_names,
                    "HasAdditionalSubjectAlternativeNames": False,
                    "Status": (
                        status
                        or random.choice(
                            [
                                "PENDING_VALIDATION",
                                "ISSUED",
                                "INACTIVE",
                                "EXPIRED",
                                "VALIDATION_TIMED_OUT",
                                "REVOKED",
                                "FAILED",
                            ]
                        )
                    ),
                    "Type": acm_type
                    or random.choice(
                        get_args(
                            ACMCertificateTypes,
                        )
                    ),
                    "KeyAlgorithm": random.choice(
                        [
                            "RSA_1024",
                            "RSA_2048",
                            "RSA_3072",
                            "RSA_4096",
                            "EC_prime256v1",
                            "EC_secp384r1",
                            "EC_secp521r1",
                        ]
                    ),
                    "KeyUsages": random.choice(
                        [
                            "DIGITAL_SIGNATURE",
                            "NON_REPUDIATION",
                            "KEY_ENCIPHERMENT",
                            "DATA_ENCIPHERMENT",
                            "KEY_AGREEMENT",
                            "CERTIFICATE_SIGNING",
                            "CRL_SIGNING",
                            "ENCIPHER_ONLY",
                            "DECIPHER_ONLY",
                            "ANY",
                            "CUSTOM",
                        ]
                    ),
                    "ExtendedKeyUsages": random.choice(
                        [
                            "TLS_WEB_SERVER_AUTHENTICATION",
                            "TLS_WEB_CLIENT_AUTHENTICATION",
                            "CODE_SIGNING",
                            "EMAIL_PROTECTION",
                            "TIME_STAMPING",
                            "OCSP_SIGNING",
                            "IPSEC_END_SYSTEM",
                            "IPSEC_TUNNEL",
                            "IPSEC_USER",
                            "ANY",
                            "NONE",
                            "CUSTOM",
                        ]
                    ),
                    "InUse": True,
                    "RenewalEligibility": "INELIGIBLE",
                    "NotBefore": _fake.past_datetime(),
                    "NotAfter": _fake.past_datetime(),
                    "CreatedAt": _fake.past_datetime(),
                    "ImportedAt": _fake.past_datetime(),
                    "RevokedAt": _fake.past_datetime(),
                }
                for j in range(_fake.pyint(1, count))
            ],
        }
        for i in range(_fake.pyint(3, count))
    )


def fake_datetime_text():
    return _fake.past_datetime().strftime(DEFAULT_DATETIME_FORMAT)


def fake_domain_name() -> str:
    return _fake.domain_name(_fake.pyint(1, _DEFAULT_RESPONSES_COUNT))
