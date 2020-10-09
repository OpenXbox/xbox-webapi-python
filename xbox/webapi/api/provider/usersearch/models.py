from typing import List

from xbox.webapi.common.models import CamelCaseModel


class UserDetail(CamelCaseModel):
    id: str
    gamertag: str
    display_pic_uri: str
    score: float


class UserResult(CamelCaseModel):
    text: str
    result: UserDetail


class UserSearchResponse(CamelCaseModel):
    results: List[UserResult]
