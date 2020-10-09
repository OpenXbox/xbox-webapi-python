from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from xbox.webapi.common.models import CamelCaseModel, PascalCaseModel


class TitleFields(str, Enum):
    SERVICE_CONFIG_ID = "scid"
    ACHIEVEMENT = "achievement"
    STATS = "stats"
    GAME_PASS = "gamepass"
    IMAGE = "image"
    DETAIL = "detail"
    FRIENDS_WHO_PLAYED = "friendswhoplayed"
    ALTERNATE_TITLE_ID = "alternateTitleId"


class Achievement(CamelCaseModel):
    current_achievements: int
    total_achievements: int
    current_gamerscore: int
    total_gamerscore: int
    progress_percentage: float
    source_version: int


class Stats(CamelCaseModel):
    source_version: int


class GamePass(CamelCaseModel):
    is_game_pass: bool


class Image(CamelCaseModel):
    url: str
    type: str


class TitleHistory(CamelCaseModel):
    last_time_played: datetime
    visible: bool
    can_hide: bool


class Attribute(CamelCaseModel):
    applicable_platforms: Optional[List[str]]
    maximum: Optional[int]
    minimum: Optional[int]
    name: str


class Availability(PascalCaseModel):
    actions: List[str]
    availability_id: str
    platforms: List[str]
    sku_id: str


class Detail(CamelCaseModel):
    attributes: List[Attribute]
    availabilities: List[Availability]
    capabilities: List[str]
    description: str
    developer_name: str
    publisher_name: str
    min_age: int
    release_date: Optional[datetime]
    short_description: Optional[str]
    vui_display_name: Optional[str]
    xbox_live_gold_required: bool


class Title(CamelCaseModel):
    title_id: str
    pfn: Optional[str]
    bing_id: Optional[str]
    service_config_id: Optional[str]
    windows_phone_product_id: Optional[str]
    name: str
    type: str
    devices: List[str]
    display_image: str
    media_item_type: str
    modern_title_id: Optional[str]
    is_bundle: bool
    achievement: Optional[Achievement]
    stats: Optional[Stats]
    game_pass: Optional[GamePass]
    images: Optional[List[Image]]
    title_history: Optional[TitleHistory]
    detail: Optional[Detail]
    friends_who_played: Any
    alternate_title_ids: Any
    content_boards: Any
    xbox_live_tier: Optional[str]
    is_streamable: Optional[bool]


class TitleHubResponse(CamelCaseModel):
    xuid: Optional[str]
    titles: List[Title]
