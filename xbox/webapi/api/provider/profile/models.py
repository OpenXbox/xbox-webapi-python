from enum import Enum
from typing import List

from xbox.webapi.common.models import CamelCaseModel


class ProfileSettings(str, Enum):
    """
    Profile settings, used as parameter for Profile API
    """

    GAME_DISPLAY_NAME = "GameDisplayName"
    APP_DISPLAY_NAME = "AppDisplayName"
    APP_DISPLAYPIC_RAW = "AppDisplayPicRaw"
    GAME_DISPLAYPIC_RAW = "GameDisplayPicRaw"
    PUBLIC_GAMERPIC = "PublicGamerpic"
    SHOW_USER_AS_AVATAR = "ShowUserAsAvatar"
    GAMERSCORE = "Gamerscore"
    GAMERTAG = "Gamertag"
    MODERN_GAMERTAG = "ModernGamertag"
    MODERN_GAMERTAG_SUFFIX = "ModernGamertagSuffix"
    UNIQUE_MODERN_GAMERTAG = "UniqueModernGamertag"
    ACCOUNT_TIER = "AccountTier"
    TENURE_LEVEL = "TenureLevel"
    XBOX_ONE_REP = "XboxOneRep"
    PREFERRED_COLOR = "PreferredColor"
    LOCATION = "Location"
    BIOGRAPHY = "Bio"
    WATERMARKS = "Watermarks"
    REAL_NAME = "RealName"
    REAL_NAME_OVERRIDE = "RealNameOverride"
    IS_QUARANTINED = "IsQuarantined"


class Setting(CamelCaseModel):
    id: str
    value: str


class ProfileUser(CamelCaseModel):
    id: str
    host_id: str
    settings: List[Setting]
    is_sponsored_user: bool


class ProfileResponse(CamelCaseModel):
    profile_users: List[ProfileUser]
