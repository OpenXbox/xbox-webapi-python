from enum import Enum
from typing import List, Optional

from pydantic import Field

from xbox.webapi.common.models import PascalCaseModel


class MediaItemType(str, Enum):
    """
    Media Item Type, used as parameter for EDS API
    """

    XBOX360_GAME = "Xbox360Game"
    XBOX360_GAME_CONTENT = "Xbox360GameContent"
    XBOX360_GAME_DEMO = "Xbox360GameDemo"

    XBOX_GAME_TRIAL = "XboxGameTrial"
    XBOX_THEME = "XboxTheme"
    XBOX_ORIGINAL_GAME = "XboxOriginalGame"
    XBOX_GAMER_TILE = "XboxGamerTile"
    XBOX_ARCADE_GAME = "XboxArcadeGame"
    XBOX_GAME_CONSUMABLE = "XboxGameConsumable"
    XBOX_GAME_VIDEO = "XboxGameVideo"
    XBOX_GAME_TRAILER = "XboxGameTrailer"
    XBOX_BUNDLE = "XboxBundle"
    XBOX_XNA_GAME = "XboxXnaCommunityGame"
    XBOX_MARKETPLACE = "XboxMarketplace"
    XBOX_APP = "XboxApp"

    XBOXONE_GAME = "DGame"
    XBOXONE_GAME_DEMO = "DGameDemo"
    XBOXONE_CONSUMABLE = "DConsumable"
    XBOXONE_DURABLE = "DDurable"
    XBOXONE_APP = "DApp"
    XBOXONE_ACTIVITY = "DActivity"
    XBOXONE_NATIVE_APP = "DNativeApp"

    METRO_GAME = "MetroGame"
    METRO_GAME_CONTENT = "MetroGameContent"
    METRO_GAME_CONSUMABLE = "MetroGameConsumable"

    AVATAR_ITEM = "AvatarItem"

    MOBILE_GAME = "MobileGame"
    XBOX_MOBILE_PDLC = "XboxMobilePDLC"
    XBOX_MOBILE_CONSUMABLE = "XboxMobileConsumable"

    TV_SHOW = "TVShow"
    TV_EPISODE = "TVEpisode"
    TV_SERIES = "TVSeries"
    TV_SEASON = "TVSeason"

    MUSIC_ALBUM = "Album"
    MUSIC_TRACK = "Track"
    MUSIC_VIDEO = "MusicVideo"
    MUSIC_ARTIST = "MusicArtist"

    WEB_GAME = "WebGame"
    WEB_VIDEO = "WebVideo"
    WEB_VIDEO_COLLECTION = "WebVideoCollection"

    GAME_LAYER = "GameLayer"
    GAME_ACTIVITY = "GameActivity"
    APP_ACTIVITY = "AppActivity"
    VIDEO_LAYER = "VideoLayer"
    VIDEO_ACTIVITY = "VideoActivity"

    SUBSCRIPTION = "Subscription"


class MediaGroup(str, Enum):
    """
    Media Group, used as parameter for EDS API

    GameType:
    Xbox360Game, XboxGameTrial, Xbox360GameContent, Xbox360GameDemo, XboxTheme, XboxOriginalGame,
    XboxGamerTile, XboxArcadeGame, XboxGameConsumable, XboxGameVideo, XboxGameTrailer, XboxBundle, XboxXnaCommunityGame,
    XboxMarketplace, AvatarItem, MobileGame, XboxMobilePDLC, XboxMobileConsumable, WebGame, MetroGame, MetroGameContent,
    MetroGameConsumable, DGame, DGameDemo, DConsumable, DDurable

    AppType: XboxApp, DApp
    MovieType: Movie
    TVType: TVShow (one-off TV shows), TVEpisode, TVSeries, TVSeason
    MusicType: Album, Track, MusicVideo
    MusicArtistType: MusicArtist
    WebVideoType: WebVideo, WebVideoCollection
    EnhancedContentType: GameLayer, GameActivity, AppActivity, VideoLayer, VideoActivity, DActivity, DNativeApp
    SubscriptionType: Subscription
    """

    GAME_TYPE = "GameType"
    APP_TYPE = "AppType"
    MOVIE_TYPE = "MovieType"
    TV_TYPE = "TVType"
    MUSIC_TYPE = "MusicType"
    MUSIC_ARTIST_TYPE = "MusicArtistType"
    WEB_VIDEO_TYPE = "WebVideoType"
    ENHANCED_CONTENT_TYPE = "EnhancedContentType"
    SUBSCRIPTION_TYPE = "SubscriptionType"


class Domain(str, Enum):
    """
    Domain, used as parameter for EDS API
    """

    XBOX_360 = "Xbox360"
    XBOX_ONE = "Modern"


class IdType(str, Enum):
    """
    ID Type, used as parameter for EDS API
    """

    CANONICAL = "Canonical"  # BING/MARKETPLACE
    XBOX_HEX_TITLE = "XboxHexTitle"
    SCOPED_MEDIA_ID = "ScopedMediaId"
    ZUNE_CATALOG = "ZuneCatalog"
    ZUNE_MEDIA_INSTANCE = "ZuneMediaInstance"
    AMG = "AMG"
    MEDIA_NET = "MediaNet"
    PROVIDER_CONTENT_ID = "ProviderContentId"  # NETFLIX/HULU


class ClientType(str, Enum):
    """
    Client Type, used as parameter for EDS API
    """

    C13 = "C13"
    COMMERCIAL_SERVICE = "CommercialService"
    COMPANION = "Companion"
    CONSOLE = "Console"
    EDITORIAL = "Editorial"
    FIRST_PARTY_APP = "1stPartyApp"
    MO_LIVE = "MoLive"
    WINDOWS_PHONE_7 = "PhoneROM"
    RECOMMENDATION_SERVICE = "RecommendationService"
    SAS = "SAS"
    SDS = "SDS"
    SUBSCRIPTION_SERVICE = "SubscriptionService"
    X8 = "X8"
    X13 = "X13"
    WEBBLEND = "Webblend"
    XBOX_COM = "XboxCom"


class DeviceType(str, Enum):
    """
    Device Type, used as parameter for EDS API
    """

    XBOX360 = "Xbox360"
    XBOXONE = "XboxDurango"
    XBOX = "Xbox"
    IOS = "iOS"
    IPHONE = "iPhone"
    IPAD = "iPad"
    ANDROID = "Android"
    ANDROID_PHONE = "AndroidPhone"
    ANDROID_SLATE = "AndroidSlate"
    WIN_PC = "WindowsPC"
    WIN_PHONE = "WindowsPhone"
    SERVICE = "Service"
    WEB = "Web"


class OrderBy(str, Enum):
    """
    The orderBy parameter determines how the items being returned should be sorted
    """

    PLAY_COUNT_DAILY = "PlayCountDaily"
    FREE_AND_PAID_COUNT_DAILY = "FreeAndPaidCountDaily"
    PAID_COUNT_ALL_TIME = "PaidCountAllTime"
    PAID_COUNT_DAILY = "PaidCountDaily"
    DIGITAL_RELEASE_DATE = "DigitalReleaseDate"
    RELEASE_DATE = "ReleaseDate"
    USER_RATINGS = "UserRatings"


class SubscriptionLevel(str, Enum):
    """
    The subscriptionLevel parameter determines the type of subscription the user has
    """

    GOLD = "gold"
    SILVER = "silver"


class EDSItem(PascalCaseModel):
    media_group: str
    media_item_type: str
    id: str = Field(alias="ID")
    name: str
    k_value: str
    k_value_namespace: str


class Total(PascalCaseModel):
    name: str
    count: int


class EDSResponse(PascalCaseModel):
    items: List[EDSItem]
    continuation_token: Optional[str]
    totals: Optional[List[Total]]
    impression_guid: str
