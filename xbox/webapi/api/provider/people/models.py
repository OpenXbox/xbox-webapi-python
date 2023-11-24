from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from xbox.webapi.common.models import CamelCaseModel, PascalCaseModel


class PeopleDecoration(str, Enum):
    SUGGESTION = "suggestion"
    RECENT_PLAYER = "recentplayer"
    FOLLOWER = "follower"
    PREFERRED_COLOR = "preferredcolor"
    DETAIL = "detail"
    MULTIPLAYER_SUMMARY = "multiplayersummary"
    PRESENCE_DETAIL = "presencedetail"
    TITLE_PRESENCE = "titlepresence"
    TITLE_SUMMARY = "titlesummary"
    PRESENCE_TITLE_IDS = "presencetitleids"
    COMMUNITY_MANAGER_TITLES = "communitymanagertitles"
    SOCIAL_MANAGER = "socialmanager"
    BROADCAST = "broadcast"
    TOURNAMENT_SUMMARY = "tournamentsummary"
    AVATAR = "avatar"


class PeopleSummaryResponse(CamelCaseModel):
    target_following_count: int
    target_follower_count: int
    is_caller_following_target: bool
    is_target_following_caller: bool
    has_caller_marked_target_as_favorite: bool
    has_caller_marked_target_as_identity_shared: bool
    legacy_friend_status: str
    available_people_slots: Optional[int] = None
    recent_change_count: Optional[int] = None
    watermark: Optional[str] = None


class Suggestion(PascalCaseModel):
    type: Optional[str] = None
    priority: int
    reasons: Optional[str] = None
    title_id: Optional[str] = None


class Recommendation(PascalCaseModel):
    type: str
    reasons: List[str]


class MultiplayerSummary(PascalCaseModel):
    in_multiplayer_session: int
    in_party: int


class RecentPlayer(CamelCaseModel):
    titles: List[str]
    text: Optional[str] = None


class Follower(CamelCaseModel):
    text: Optional[str] = None
    followed_date_time: Optional[datetime] = None


class PreferredColor(CamelCaseModel):
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    tertiary_color: Optional[str] = None


class PresenceDetail(PascalCaseModel):
    is_broadcasting: bool
    device: str
    presence_text: str
    state: str
    title_id: str
    title_type: Optional[str] = None
    is_primary: bool
    is_game: bool
    rich_presence_text: Optional[str] = None


class TitlePresence(PascalCaseModel):
    is_currently_playing: bool
    presence_text: Optional[str] = None
    title_name: Optional[str] = None
    title_id: Optional[str] = None


class Detail(CamelCaseModel):
    account_tier: str
    bio: Optional[str] = None
    is_verified: bool
    location: Optional[str] = None
    tenure: Optional[str] = None
    watermarks: List[str]
    blocked: bool
    mute: bool
    follower_count: int
    following_count: int
    has_game_pass: bool


class SocialManager(CamelCaseModel):
    title_ids: List[str]
    pages: List[str]


class Avatar(CamelCaseModel):
    update_time_offset: Optional[datetime] = None
    spritesheet_metadata: Optional[Any] = None


class LinkedAccount(CamelCaseModel):
    network_name: str
    display_name: Optional[str] = None
    show_on_profile: bool
    is_family_friendly: bool
    deeplink: Optional[str] = None


class Person(CamelCaseModel):
    xuid: str
    is_favorite: bool
    is_following_caller: bool
    is_followed_by_caller: bool
    is_identity_shared: bool
    added_date_time_utc: Optional[datetime] = None
    display_name: Optional[str] = None
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
    presence_devices: Optional[Any] = None
    is_broadcasting: bool
    is_cloaked: Optional[bool] = None
    is_quarantined: bool
    is_xbox_360_gamerpic: bool
    last_seen_date_time_utc: Optional[datetime] = None
    suggestion: Optional[Suggestion] = None
    recommendation: Optional[Recommendation] = None
    search: Optional[Any] = None
    titleHistory: Optional[Any] = None
    multiplayer_summary: Optional[MultiplayerSummary] = None
    recent_player: Optional[RecentPlayer] = None
    follower: Optional[Follower] = None
    preferred_color: Optional[PreferredColor] = None
    presence_details: Optional[List[PresenceDetail]] = None
    title_presence: Optional[TitlePresence] = None
    title_summaries: Optional[Any] = None
    presence_title_ids: Optional[List[str]] = None
    detail: Optional[Detail] = None
    community_manager_titles: Optional[Any] = None
    social_manager: Optional[SocialManager] = None
    broadcast: Optional[List[Any]] = None
    tournament_summary: Optional[Any] = None
    avatar: Optional[Avatar] = None
    linked_accounts: Optional[List[LinkedAccount]] = None
    color_theme: str
    preferred_flag: str
    preferred_platforms: List[Any]


class RecommendationSummary(CamelCaseModel):
    friend_of_friend: int
    facebook_friend: int
    phone_contact: int
    follower: int
    VIP: int
    steam_friend: int
    promote_suggestions: bool


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


class PeopleResponse(CamelCaseModel):
    people: List[Person]
    recommendation_summary: Optional[RecommendationSummary] = None
    friend_finder_state: Optional[FriendFinderState] = None
    account_link_details: Optional[List[LinkedAccount]] = None
