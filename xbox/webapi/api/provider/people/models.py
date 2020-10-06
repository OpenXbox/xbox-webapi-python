from typing import List, Optional

from xbox.webapi.common.models import CamelCaseModel


class PeopleSummaryResponse(CamelCaseModel):
    target_following_Count: int
    target_follower_Count: int
    is_caller_following_target: bool
    is_target_following_caller: bool
    has_caller_marked_target_as_favorite: bool
    has_caller_marked_target_as_known: bool
    legacy_friend_status: str
    available_people_slots: Optional[int]
    recent_change_count: Optional[int]
    watermark: Optional[str]


class Person(CamelCaseModel):
    xuid: str
    added_date_time_utc: str
    is_favorite: bool
    is_known: bool
    social_networks: List
    is_followed_by_caller: bool
    is_following_caller: bool
    is_unfollowing_feed: bool


class PeopleResponse(CamelCaseModel):
    total_count: int
    people: List[Person]
