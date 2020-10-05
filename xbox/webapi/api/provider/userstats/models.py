from typing import List, Optional

from pydantic import BaseModel

from xbox.webapi.common.models import PascalCaseModel


class GeneralStatsField:
    MINUTES_PLAYED = "MinutesPlayed"


class GroupProperties(PascalCaseModel):
    Ordinal: str
    SortOrder: str
    DisplayName: str
    DisplayFormat: str
    DisplaySemantic: str


class Properties(PascalCaseModel):
    DisplayName: str


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
    titleid: str
    statlistscollection: List[StatlistscollectionItem]


class UserstatsResponse(BaseModel):
    groups: Optional[List[Group]]
    statlistscollection: List[StatlistscollectionItem]
