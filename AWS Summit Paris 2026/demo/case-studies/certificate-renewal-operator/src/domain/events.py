"""
Provides business domain models defined using the pydantic library

Topics
- Learn more about how to use pydantic, checkout this video https://www.youtube.com/watch?v=7aBRk_JP-qY
"""

from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from domain.types import DomainName

EventDetailType = Literal["ACM Certificate Approaching Expiration"]
EventSource = Literal["aws.acm"]

RegionName = Literal["eu-central-1"]


class EventDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    days_to_expiry: int = Field(alias="DaysToExpiry")
    common_name: DomainName = Field(alias="CommonName")


class CertificateApproachingExpirationEvent(BaseModel):
    version: str
    id: str
    detail_type: EventDetailType = Field(alias="detail-type")
    source: EventSource
    account: str
    time: datetime
    region: RegionName
    resources: List[str]
    detail: EventDetail
