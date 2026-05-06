from domain.models import Certificate


def test_tag_certificate_with_new_key():
    certificate = Certificate.of_common_name("example.com")
    tagged = certificate.tag(
        "saws.security:cert-mgt.cro/sectigo.certmanager.id", "1234"
    )

    assert tagged is True


def test_tag_certificate_with_exiting_key():
    existing_key = "saws.security:cert-mgt.cro/sectigo.certmanager.id"
    certificate = Certificate.of_common_name("example.com")
    certificate.tag(existing_key, "1234")

    tagged_twice = certificate.tag(existing_key, "0000")

    assert tagged_twice is True
    assert certificate.tags.get(existing_key) == "0000"
