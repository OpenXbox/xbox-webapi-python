from typing import Any, Dict, List, Optional

from xbox.webapi.common.models import CamelCaseModel


class Image(CamelCaseModel):
    purpose: str
    resize_uri: str
    fore_color: str


class ListChannel(CamelCaseModel):
    id: str
    channel_id: str
    call_sign: str
    channel_number: str
    start_date: str
    end_date: str
    images: List[Image]
    is_HD: Optional[bool] = None


class CqsChannelListResponse(CamelCaseModel):
    channels: List[ListChannel]


class Genre(CamelCaseModel):
    name: str


class ParentSeries(CamelCaseModel):
    id: str
    name: str


class Program(CamelCaseModel):
    id: str
    media_item_type: str
    start_date: str
    end_date: str
    name: str
    is_repeat: bool
    parental_control: Dict[str, Any]
    genres: List[Genre]
    category_id: int
    description: Optional[str] = None
    parent_series: Optional[ParentSeries] = None
    images: Optional[List[Image]] = None


class ScheduleChannel(CamelCaseModel):
    id: str
    name: str
    images: List[Image]
    programs: List[Program]


class CqsScheduleResponse(CamelCaseModel):
    channels = List[ScheduleChannel]
