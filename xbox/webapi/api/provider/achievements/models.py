from datetime import datetime, time
from typing import Any, List, Optional

from pydantic import BaseModel

from xbox.webapi.common.models import CamelCaseModel


class PagingInfo(CamelCaseModel):
    continuation_token: Optional[str]
    total_records: int


class Achievement360(CamelCaseModel):
    id: int
    title_id: int
    name: str
    sequence: int
    flags: int
    unlocked_online: bool
    unlocked: bool
    is_secret: bool
    platform: int
    gamerscore: int
    image_id: int
    description: str
    locked_description: str
    type: int
    is_revoked: bool
    time_unlocked: datetime


class Title360(CamelCaseModel):
    last_played: datetime
    current_achievements: int
    current_gamerscore: int
    sequence: int
    title_id: int
    title_type: int
    platforms: List[int]
    name: str
    total_achievements: int
    total_gamerscore: int


class Achievement360Response(CamelCaseModel):
    achievements: List[Achievement360]
    paging_info: PagingInfo
    version: datetime


class Achievement360ProgressResponse(CamelCaseModel):
    titles: List[Title360]
    paging_info: PagingInfo
    version: datetime


class TitleAssociation(BaseModel):
    name: str
    id: int


class Requirement(CamelCaseModel):
    id: str
    current: Optional[str]
    target: str
    operation_type: str
    value_type: str
    rule_participation_type: str


class Progression(CamelCaseModel):
    requirements: List[Requirement]
    time_unlocked: datetime


class MediaAsset(BaseModel):
    name: str
    type: str
    url: str


class Reward(CamelCaseModel):
    name: Any
    description: Any
    value: str
    type: str
    media_asset: Any
    value_type: str


class Achievement(CamelCaseModel):
    id: str
    service_config_id: str
    name: str
    title_associations: List[TitleAssociation]
    progress_state: str
    progression: Progression
    media_assets: List[MediaAsset]
    platforms: List[str]
    is_secret: bool
    description: str
    locked_description: str
    product_id: str
    achievement_type: str
    participation_type: str
    time_window: Any
    rewards: List[Reward]
    estimated_time: time
    deeplink: Any
    is_revoked: bool


class AchievementResponse(CamelCaseModel):
    achievements: List[Achievement]
    paging_info: PagingInfo


class Title(CamelCaseModel):
    last_unlock: datetime
    title_id: int
    service_config_id: str
    title_type: str
    platform: str
    name: str
    earned_achievements: int
    current_gamerscore: int
    max_gamerscore: int


class RecentProgressResponse(CamelCaseModel):
    titles: List[Title]
    paging_info: PagingInfo
