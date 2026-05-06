from datetime import datetime

from application.certificate_renewal.certificate_approaching_expiration_event import (
    CertificateApproachingExpirationEvent,
)


def test_parse_certificate_approaching_expiration_event():
    # Arrange
    input = {
        "version": "0",
        "id": "9c95e8e4-96a4-ef3f-b739-b6aa5b193afb",
        "detail-type": "ACM Certificate Approaching Expiration",
        "source": "aws.acm",
        "account": "123456789012",
        "time": "2020-09-30T06:51:08Z",
        "region": "eu-central-1",
        "resources": [
            "arn:aws:acm:us-east-1:123456789012:certificate/61f50cd4-45b9-4259-b049-d0a53682fa4b"
        ],
        "detail": {"DaysToExpiry": 31, "CommonName": "example.com"},
    }

    # Act
    event = CertificateApproachingExpirationEvent(**input)

    # Assert
    assert event.version == input["version"]
    assert event.id == input["id"]
    assert event.detail_type == input["detail-type"]
    assert event.source == input["source"]
    assert event.account == input["account"]
    assert event.time == datetime.fromisoformat(input["time"])
    assert event.region == input["region"]
    assert event.resources == input["resources"]
    assert event.detail.days_to_expiry == input["detail"]["DaysToExpiry"]
    assert event.detail.common_name == input["detail"]["CommonName"]
