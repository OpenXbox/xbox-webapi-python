from typing import List, Optional

from xbox.webapi.common.models import LowerCaseModel, PascalCaseModel


class GeneralStatsField:
    MINUTES_PLAYED = "MinutesPlayed"


class GroupProperties(PascalCaseModel):
    ordinal: Optional[str]
    sort_order: Optional[str]
    display_name: Optional[str]
    display_format: Optional[str]
    display_semantic: Optional[str]


class Properties(PascalCaseModel):
    display_name: Optional[str]


class Stat(LowerCaseModel):
    group_properties: Optional[GroupProperties]
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
    title_id: Optional[str]
    statlistscollection: List[StatListsCollectionItem]


class UserStatsResponse(LowerCaseModel):
    groups: Optional[List[Group]]
    statlistscollection: List[StatListsCollectionItem]
