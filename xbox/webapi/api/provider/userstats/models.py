from typing import List, Optional

from pydantic import BaseModel

from xbox.webapi.common.models import PascalCaseModel


class GeneralStatsField:
    MINUTES_PLAYED = "MinutesPlayed"


class GroupProperties(PascalCaseModel):
    Ordinal: Optional[str]
    SortOrder: Optional[str]
    DisplayName: Optional[str]
    DisplayFormat: Optional[str]
    DisplaySemantic: Optional[str]


class Properties(PascalCaseModel):
    DisplayName: Optional[str]


class Stat(BaseModel):
    groupproperties: Optional[GroupProperties]
    xuid: str
    scid: str
    name: str
    type: str
    value: str
    properties: Properties


class StatlistscollectionItem(BaseModel):
    arrangebyfield: str
    arrangebyfieldid: str
    stats: List[Stat]


class Group(BaseModel):
    name: str
    titleid: Optional[str]
    statlistscollection: List[StatlistscollectionItem]


class UserstatsResponse(BaseModel):
    groups: Optional[List[Group]]
    statlistscollection: List[StatlistscollectionItem]
