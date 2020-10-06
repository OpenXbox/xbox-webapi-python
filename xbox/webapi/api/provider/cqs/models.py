from typing import Any, Dict, List, Optional

from xbox.webapi.common.models import PascalCaseModel


class Image(PascalCaseModel):
    purpose: str
    resize_uri: str
    fore_color: str


class ListChannel(PascalCaseModel):
    id: str
    channel_id: str
    call_sign: str
    channel_number: str
    start_date: str
    end_date: str
    images: List[Image]
    is_HD: Optional[bool] = None


class CqsChannelListResponse(PascalCaseModel):
    channels: List[ListChannel]


class Genre(PascalCaseModel):
    name: str


class ParentSeries(PascalCaseModel):
    id: str
    name: str


class Program(PascalCaseModel):
    id: str
    media_item_type: str
    start_date: str
    end_date: str
    name: str
    is_repeat: bool
    parental_control: Optional[Dict[str, Any]]
    genres: List[Genre]
    category_id: int
    description: Optional[str] = None
    parent_series: Optional[ParentSeries] = None
    images: Optional[List[Image]] = None


class ScheduleChannel(PascalCaseModel):
    id: str
    name: str
    images: List[Image]
    programs: List[Program]


class CqsScheduleResponse(PascalCaseModel):
    channels: List[ScheduleChannel]
