from typing import List, Optional

from xbox.webapi.common.models import CamelCaseModel


class ContentSegment(CamelCaseModel):
    segment_id: int
    creation_type: str
    creator_channel_id: Optional[str] = None
    creator_xuid: int
    record_date: str
    duration_in_seconds: int
    offset: int
    secondary_title_id: Optional[int] = None
    title_id: int


class ContentLocator(CamelCaseModel):
    expiration: Optional[str] = None
    file_size: Optional[int] = None
    locator_type: str
    uri: str


class GameclipContent(CamelCaseModel):
    content_id: str
    content_locators: List[ContentLocator]
    content_segments: List[ContentSegment]
    creation_type: str
    duration_in_seconds: int
    local_id: str
    owner_xuid: int
    sandbox_id: str
    shared_to: List[int]
    title_id: int
    title_name: str
    upload_date: str
    upload_language: str
    upload_region: str
    upload_title_id: int
    upload_device_type: str
    comment_count: int
    like_count: int
    share_count: int
    view_count: int
    content_state: str
    enforcement_state: str
    sessions: List[str]
    tournaments: List[str]


class MediahubGameclips(CamelCaseModel):
    values: List[GameclipContent]


class ScreenshotContent(CamelCaseModel):
    content_id: str
    capture_date: str
    content_locators: List[ContentLocator]
    local_id: str
    owner_xuid: int
    resolution_height: int
    resolution_width: int
    date_uploaded: str
    sandbox_id: str
    shared_to: List[int]
    title_id: int
    title_name: str
    upload_language: str
    upload_region: str
    upload_title_id: int
    upload_device_type: str
    comment_count: int
    like_count: int
    share_count: int
    view_count: int
    content_state: str
    enforcement_state: str
    sessions: List[str]
    tournaments: List[str]


class MediahubScreenshots(CamelCaseModel):
    values: List[ScreenshotContent]
