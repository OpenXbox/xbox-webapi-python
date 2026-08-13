
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import Field

from xbox.webapi.common.models import CamelCaseModel, PascalCaseModel


class PeopleDecoration(StrEnum):
    SUGGESTION = "suggestion"
    RECENT_PLAYER = "recentPlayer"
    FOLLOWER = "follower"
    PREFERRED_COLOR = "preferredColor"
    DETAIL = "detail"
    MULTIPLAYER_SUMMARY = "multiplayerSummary"
    PRESENCE_DETAIL = "presenceDetail"
    TITLE_PRESENCE = "titlePresence"
    TITLE_SUMMARY = "titleSummary"
    PRESENCE_TITLE_IDS = "presenceTitleIds"
    COMMUNITY_MANAGER_TITLES = "communityManagerTitles"
    SOCIAL_MANAGER = "socialManager"
    BROADCAST = "broadcast"
    TOURNAMENT_SUMMARY = "tournamentSummary"
    AVATAR = "avatar"


class PeopleSummaryResponse(CamelCaseModel):
    target_following_count: int
    target_follower_count: int
    is_caller_following_target: bool
    is_target_following_caller: bool
    has_caller_marked_target_as_favorite: bool
    has_caller_marked_target_as_identity_shared: bool
    legacy_friend_status: str
    available_people_slots: int | None = None
    recent_change_count: int | None = None
    watermark: str | None = None
    is_friend: bool


class Suggestion(PascalCaseModel):
    type: str | None = None
    priority: int
    reasons: str | None = None
    title_id: str | None = None


class Recommendation(PascalCaseModel):
    type: str
    reasons: list[str]

class SessionRef(CamelCaseModel):
    scid: str
    template_name: str
    name: str

class PartyDetails(CamelCaseModel):
    session_ref: SessionRef
    status: str
    visibility: str
    join_restriction: str
    accepted: int

class MultiplayerSummary(CamelCaseModel):
    in_multiplayer_session: int | None = None
    in_party: int
    joinable_activities: list = Field(default_factory=list)
    party_details: list[PartyDetails] = Field(default_factory=list)


class RecentPlayer(CamelCaseModel):
    titles: list[str]
    text: str | None = None


class Follower(CamelCaseModel):
    text: str | None = None
    followed_date_time_utc: datetime | None  = None


class PreferredColor(CamelCaseModel):
    primary_color: str | None = None
    secondary_color: str | None = None
    tertiary_color: str | None = None


class PresenceDetail(PascalCaseModel):
    is_broadcasting: bool
    device: str
    device_sub_type: str | None = None
    gameplay_type: str | None = None
    presence_text: str
    state: str
    title_id: str
    title_type: str | None = None
    is_primary: bool
    is_game: bool
    rich_presence_text: str | None = None


class TitlePresence(PascalCaseModel):
    is_currently_playing: bool
    presence_text: str | None = None
    title_name: str | None = None
    title_id: str | None = None


class Detail(CamelCaseModel):
    account_tier: str
    bio: str | None = None
    is_verified: bool
    location: str | None = None
    tenure: str | None = None
    watermarks: list[str]
    blocked: bool
    mute: bool
    follower_count: int
    following_count: int
    has_game_pass: bool
    can_be_friended: bool
    can_be_followed: bool
    is_friend: bool
    friend_count: int
    is_friend_request_received: bool
    is_friend_request_sent: bool
    is_friend_list_shared: bool
    is_following_caller: bool
    is_followed_by_caller: bool
    is_favorite: bool


class SocialManager(CamelCaseModel):
    title_ids: list[str]
    pages: list[str]


class Avatar(CamelCaseModel):
    update_time_offset: datetime | None  = None
    spritesheet_metadata: Any | None = None


class LinkedAccount(CamelCaseModel):
    network_name: str
    display_name: str | None = None
    show_on_profile: bool
    is_family_friendly: bool
    deeplink: str | None = None


class Person(CamelCaseModel):
    xuid: str
    is_favorite: bool
    is_following_caller: bool
    is_followed_by_caller: bool
    is_identity_shared: bool
    added_date_time_utc: datetime | None  = None
    display_name: str | None = None
    real_name: str
    display_pic_raw: str
    show_user_as_avatar: str
    gamertag: str
    gamer_score: str
    modern_gamertag: str
    modern_gamertag_suffix: str
    unique_modern_gamertag: str
    xbox_one_rep: str
    presence_state: str
    presence_text: str
    presence_devices: Any | None = None
    is_broadcasting: bool
    is_cloaked: bool | None = None
    is_quarantined: bool
    is_xbox_360_gamerpic: bool
    last_seen_date_time_utc: datetime | None  = None
    suggestion: Suggestion | None = None
    recommendation: Recommendation | None = None
    search: Any | None = None
    titleHistory: Any | None = None
    multiplayer_summary: MultiplayerSummary | None = None
    recent_player: RecentPlayer | None = None
    follower: Follower | None = None
    preferred_color: PreferredColor | None = None
    presence_details: list[PresenceDetail] | None = None
    title_presence: TitlePresence | None = None
    title_summaries: Any | None = None
    presence_title_ids: list[str] | None = None
    detail: Detail | None = None
    community_manager_titles: Any | None = None
    social_manager: SocialManager | None = None
    broadcast: list[Any] | None = None
    tournament_summary: Any | None = None
    avatar: Avatar | None = None
    linked_accounts: list[LinkedAccount] | None = None
    color_theme: str
    preferred_flag: str
    preferred_platforms: list[Any]
    friended_date_time_utc: datetime | None = None
    is_friend: bool
    is_friend_request_received: bool
    is_friend_request_sent: bool
    


class RecommendationSummary(CamelCaseModel):
    friend_of_friend: int | None = None
    facebook_friend: int | None = None
    phone_contact: int | None = None
    follower: int | None = None
    VIP: int | None = None
    steam_friend: int
    promote_suggestions: bool
    community_suggestion: int
    


class FriendFinderState(CamelCaseModel):
    facebook_opt_in_status: str
    facebook_token_status: str
    phone_opt_in_status: str
    phone_token_status: str
    steam_opt_in_status: str
    steam_token_status: str
    discord_opt_in_status: str
    discord_token_status: str
    instagram_opt_in_status: str
    instagram_token_status: str
    mixer_opt_in_status: str
    mixer_token_status: str
    reddit_opt_in_status: str
    reddit_token_status: str
    twitch_opt_in_status: str
    twitch_token_status: str
    twitter_opt_in_status: str
    twitter_token_status: str
    you_tube_opt_in_status: str
    you_tube_token_status: str

class FriendRequestSummary(CamelCaseModel):
    friend_requests_received_count: int

class PeopleResponse(CamelCaseModel):
    people: list[Person]
    recommendation_summary: RecommendationSummary | None = None
    friend_finder_state: FriendFinderState | None = None
    account_link_details: list[LinkedAccount] | None = None
    friend_request_summary: FriendRequestSummary | None = None