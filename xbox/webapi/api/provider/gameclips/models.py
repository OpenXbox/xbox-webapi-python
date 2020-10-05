from typing import List

from xbox.webapi.common.models import CamelCaseModel


class Thumbnail(CamelCaseModel):
    uri: str
    file_size: int
    thumbnail_type: str


class GameClipUri(CamelCaseModel):
    uri: str
    file_size: int
    uri_type: str
    expiration: str


class GameClip(CamelCaseModel):
    game_clip_id: str
    state: str
    date_published: str
    date_recorded: str
    last_modified: str
    user_caption: str
    type: str
    duration_in_seconds: int
    scid: str
    title_id: int
    rating: float
    rating_count: int
    views: int
    title_data: str
    system_properties: str
    saved_by_user: bool
    achievement_id: str
    greatest_moment_id: str
    thumbnails: List[Thumbnail]
    game_clip_uris: List[GameClipUri]
    xuid: str
    clip_name: str
    title_name: str
    game_clip_locale: str
    clip_content_attributes: str
    device_type: str
    comment_count: int
    like_count: int
    share_count: int
    partial_views: int


class PagingInfo(CamelCaseModel):
    continuation_token: str


class GameclipsResponse(CamelCaseModel):
    game_clips: List[GameClip]
    paging_info: PagingInfo
