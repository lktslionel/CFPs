from typing import Annotated, Literal

from pydantic import StringConstraints

TAG_NS = "saws.security:cert-mgt.cro"

AllowedCertificateTagKeys = Literal[
    "saws.security:cert-mgt.cro/sectigo.certmanager.id",
]

KeyValuePairs = dict[AllowedCertificateTagKeys, str]


DomainName = Annotated[
    str,
    StringConstraints(
        pattern=r"^(?:\*\.){0,1}(?:(?:\w[\w-]{0,61}\w\.)+)\w[\w-]{0,61}\w$"
    ),
]

CertificatePoviderStr = Literal["sectigo.certmanager", "aws.acm"]
