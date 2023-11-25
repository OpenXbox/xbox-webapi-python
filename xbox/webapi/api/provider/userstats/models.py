from typing import List, Optional

from xbox.webapi.common.models import LowerCaseModel, PascalCaseModel


class GeneralStatsField:
    MINUTES_PLAYED = "MinutesPlayed"


class GroupProperties(PascalCaseModel):
    ordinal: Optional[str] = None
    sort_order: Optional[str] = None
    display_name: Optional[str] = None
    display_format: Optional[str] = None
    display_semantic: Optional[str] = None


class Properties(PascalCaseModel):
    display_name: Optional[str] = None


class Stat(LowerCaseModel):
    group_properties: Optional[GroupProperties] = None
    xuid: str
    scid: str
    name: str
    type: str
    value: str
    properties: Properties


class StatListsCollectionItem(LowerCaseModel):
    arrange_by_field: str
    arrange_by_field_id: str
    stats: List[Stat]


class Group(LowerCaseModel):
    name: str
    title_id: Optional[str] = None
    statlistscollection: List[StatListsCollectionItem]


class UserStatsResponse(LowerCaseModel):
    groups: Optional[List[Group]] = None
    statlistscollection: List[StatListsCollectionItem]
