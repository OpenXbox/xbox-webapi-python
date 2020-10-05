from typing import Any, List, Optional

from xbox.webapi.common.models import CamelCaseModel


class TitleFields:
    ACHIEVEMENT = "achievement"
    IMAGE = "image"
    FRIENDS_WHO_PLAYED = "friendswhoplayed"
    SERVICE_CONFIG_ID = "SCID"
    DETAIL = "detail"
    ALTERNATE_TITLE_ID = "alternateTitleId"


class Achievement(CamelCaseModel):
    current_achievements: int
    total_achievements: int
    current_gamerscore: int
    total_gamerscore: int
    progress_percentage: float
    source_version: int


class Image(CamelCaseModel):
    url: str
    type: str


class Detail(CamelCaseModel):
    description: str
    short_description: Optional[str]
    publisher_name: str
    developer_name: str
    vui_display_name: Any
    release_date: str
    min_age: int


class Title(CamelCaseModel):
    title_id: str
    pfn: str
    bing_id: Any
    service_config_id: str
    windows_phone_product_id: str
    name: str
    type: str
    devices: List[str]
    display_image: str
    media_item_type: str
    modern_title_id: str
    is_bundle: bool
    achievement: Achievement
    stats: Any
    images: List[Image]
    title_history: Any
    detail: Optional[Detail]
    friends_who_played: Any
    alternate_title_ids: Any
    content_boards: Any
    xbox_live_tier: str


class TitlehubResponse(CamelCaseModel):
    xuid: Any
    titles: List[Title]
