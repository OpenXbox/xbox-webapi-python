from datetime import datetime
from typing import Any, List, Optional

from xbox.webapi.common.models import CamelCaseModel


class Thumbnail(CamelCaseModel):
    uri: str
    file_size: int
    thumbnail_type: int


class ScreenshotUri(CamelCaseModel):
    uri: str
    file_size: int
    uri_type: int
    expiration: datetime


class Screenshot(CamelCaseModel):
    screenshot_id: str
    resolution_height: int
    resolution_width: int
    state: int
    date_published: datetime
    date_taken: datetime
    last_modified: datetime
    user_caption: str
    type: int
    scid: str
    title_id: int
    rating: float
    rating_count: int
    views: int
    title_data: str
    system_properties: str
    saved_by_user: bool
    achievement_id: str
    greatest_moment_id: Any = None
    thumbnails: List[Thumbnail]
    screenshot_uris: List[ScreenshotUri]
    xuid: str
    screenshot_name: str
    title_name: str
    screenshot_locale: str
    screenshot_content_attributes: int
    device_type: str


class PagingInfo(CamelCaseModel):
    continuation_token: Optional[str] = None


class ScreenshotResponse(CamelCaseModel):
    screenshots: List[Screenshot]
    paging_info: PagingInfo
