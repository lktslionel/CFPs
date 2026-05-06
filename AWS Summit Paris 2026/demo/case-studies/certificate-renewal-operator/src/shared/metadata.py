from typing import Literal

AllowedMetadataKeys = Literal["correlation-id", "transaction-id"]


Metadata = dict[AllowedMetadataKeys, str]
