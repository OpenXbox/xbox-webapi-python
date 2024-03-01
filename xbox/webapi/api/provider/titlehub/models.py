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
    PRODUCT_ID = "productId"
    CONTENT_BOARD = "contentBoard"


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
    applicable_platforms: Optional[List[str]] = None
    maximum: Optional[int] = None
    minimum: Optional[int] = None
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
    genres: Optional[List[str]] = None
    publisher_name: str
    min_age: Optional[int] = None
    release_date: Optional[datetime] = None
    short_description: Optional[str] = None
    vui_display_name: Optional[str] = None
    xbox_live_gold_required: bool


class Title(CamelCaseModel):
    title_id: str
    pfn: Optional[str] = None
    bing_id: Optional[str] = None
    service_config_id: Optional[str] = None
    windows_phone_product_id: Optional[str] = None
    name: str
    type: str
    devices: List[str]
    display_image: str
    media_item_type: str
    modern_title_id: Optional[str] = None
    is_bundle: bool
    achievement: Optional[Achievement] = None
    stats: Optional[Stats] = None
    game_pass: Optional[GamePass] = None
    images: Optional[List[Image]] = None
    title_history: Optional[TitleHistory] = None
    detail: Optional[Detail] = None
    friends_who_played: Any = None
    alternate_title_ids: Any = None
    content_boards: Any = None
    xbox_live_tier: Optional[str] = None
    is_streamable: Optional[bool] = None


class TitleHubResponse(CamelCaseModel):
    xuid: Optional[str] = None
    titles: List[Title]
