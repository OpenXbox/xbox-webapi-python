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
    
class ActivityRecord(CamelCaseModel):
    richPresence: str
    media: str
    
class TitleRecord(CamelCaseModel):
    id: str
    name: str
    activity: Optional[List[ActivityRecord]]
    lastModified: str
    placement: str
    state: str

class DeviceRecord(CamelCaseModel):
    titles: List[TitleRecord]
    type: str
        

class PresenceItem(CamelCaseModel):
    xuid: str
    state: str
    last_seen: Optional[LastSeen]
    devices: Optional[List[DeviceRecord]]
    

class PresenceBatchResponse(CamelCaseModel):
    __root__: List[PresenceItem]
