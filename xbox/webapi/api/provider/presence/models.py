from enum import Enum
from typing import List, Optional

from xbox.webapi.common.models import CamelCaseModel


class PresenceLevel(str, Enum):
    USER = "user"
    DEVICE = "device"
    TITLE = "title"
    ALL = "all"


class LastSeen(CamelCaseModel):
    device_type: str
    title_id: str
    title_name: str
    timestamp: str


class PresenceItem(CamelCaseModel):
    xuid: str
    state: str
    last_seen: Optional[LastSeen]


class PresenceBatchResponse(CamelCaseModel):
    __root__: List[PresenceItem]
