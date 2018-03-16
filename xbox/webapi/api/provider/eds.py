"""
EDS (Entertainment Discovery Services)

Used for searching the Xbox Live Marketplace
"""

from xbox.webapi.common.enum import Enum


class EDSProvider(object):
    EDS_URL = "https://eds.xboxlive.com"
    HEADERS_EDS = {
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Pragma': 'no-cache',
        'x-xbl-client-type': 'Companion',
        'x-xbl-client-version': '2.0',
        'x-xbl-contract-version': '3.2',
        'x-xbl-device-type': 'WindowsPhone',
        'x-xbl-isautomated-client': 'true'
    }

    SEPERATOR = "."

    def __init__(self, client):
        """
        Initialize an instance of EDSProvider

        Args:
            client (:class:`XboxLiveClient`): Instance of XboxLiveClient
        """
        self.client = client

    def get_stump_tv_channel_list(self, lineup_id):
        """
        Get Stump (Xbox One LiveTV) channel list

        Args:
            lineup_id (str): Lineup ID

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.EDS_URL + "/media/%s/tvchannels?" % self.client.language.locale
        params = {"channelLineupId": lineup_id}
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_stump_tv_schedule(self, lineup_id, start_time, end_time, max_items, skip_items):
        """
        Get Stump (Xbox One LiveTV) schedule / EPG

        Args:
            lineup_id (str): Lineup ID
            start_time (str): Start time (format: 2016-07-11T21:50:00.000Z)
            end_time (str): End time (format: 2016-07-11T21:50:00.000Z)
            max_items (int): Maximum number of items
            skip_items (int): Count of items to skip

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.EDS_URL + "/media/%s/tvchannellineupguide?" % self.client.language.locale
        desired = [
            ScheduleDetailsField.ID,
            ScheduleDetailsField.NAME,
            ScheduleDetailsField.IMAGES,
            ScheduleDetailsField.DESCRIPTION,
            ScheduleDetailsField.PARENTAL_RATING,
            ScheduleDetailsField.PARENT_SERIES,
            ScheduleDetailsField.SCHEDULE_INFO
        ]
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "maxItems": max_items,
            "skipItems": skip_items,
            "channelLineupId": lineup_id,
            "desired": self.SEPERATOR.join(desired)
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_browse_query(self, order_by, max_items, skip_items, **kwargs):
        """
        Get a browse query

        Args:
            order_by (str): Fieldname to use for sorting the result
            max_items (int): Maximum itemcount
            skip_items (int): Count of items to skip
            **kwargs: Additional query parameters

        Returns:

        """
        url = self.EDS_URL + "/media/%s/browse?" % self.client.language.locale
        params = {
            "orderBy": order_by,
            "maxItems": max_items,
            "skipItems": skip_items
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_recommendations(self, desired, **kwargs):
        """
        Get recommended content suggestions

        Args:
            desired (str/list): Desired Media Item Types, members of (:class:`MediaItemType`)
            **kwargs: Additional query parameters

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if isinstance(desired, list):
            desired = self.SEPERATOR.join(desired)

        url = self.EDS_URL + "/media/%s/recommendations?" % self.client.language.locale
        params = {
            "desiredMediaItemTypes": desired
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_related(self, id, desired, media_item_type, **kwargs):
        """
        Get related content for a specific Id

        Args:
            id (str): Id of original content to get related content for
            desired (str/list): Desired Media Item Types, members of (:class:`MediaItemType`)
            media_item_type (str): Media item type of original id, member of (:class:`MediaItemType`)
            **kwargs: Additional query parameters

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if isinstance(desired, list):
            desired = self.SEPERATOR.join(desired)

        url = self.EDS_URL + "/media/%s/related?" % self.client.language.locale
        params = {
            "id": id,
            "desiredMediaItemTypes": desired,
            "MediaItemType": media_item_type
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_fields(self, desired, **kwargs):
        """
        Get Fields

        Args:
            desired (str): Desired
            **kwargs: Additional query parameters

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if isinstance(desired, list):
            desired = self.SEPERATOR.join(desired)

        url = self.EDS_URL + "/media/%s/fields?" % self.client.language.locale
        params = {
            "desired": desired
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_details(self, ids, mediagroup, **kwargs):
        """
        Get details for a list of IDs in a specific media group

        Args:
            ids (str/list): List of ids to get details for
            mediagroup (str): Member of :class:`MediaGroup`
            **kwargs: Additional query parameters

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if isinstance(ids, list):
            ids = self.SEPERATOR.join(ids)

        url = self.EDS_URL + "/media/%s/details?" % self.client.language.locale
        params = {
            "ids": ids,
            "MediaGroup": mediagroup
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_crossmediagroup_search(self, search_query, max_items, media_item_types, target_devices, **kwargs):
        """
        Do a crossmedia-group search (search for content for multiple devices)

        Args:
            search_query (str): Query string
            max_items (int): Maximum itemcount
            media_item_types (str/list): Desired Media Item Types, members of (:class:`MediaItemType`)
            target_devices (str): List of target devices, members of (:class:`DeviceType`)
            **kwargs: Additional query parameters

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if isinstance(media_item_types, list):
            media_item_types = self.SEPERATOR.join(media_item_types)
        url = self.EDS_URL + "/media/%s/crossMediaGroupSearch?" % self.client.language.locale
        params = {
            "q": search_query,
            "maxItems": max_items,
            "desiredMediaItemTypes": media_item_types,
            "targetDevices": target_devices

        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_singlemediagroup_search(self, search_query, max_items, media_item_types, **kwargs):
        """
        Do a singlemedia-group search

        Args:
            search_query (str): Query string
            max_items (int): Maximum itemcount
            media_item_types (str/list): Desired Media Item Types, members of (:class:`MediaItemType`)
            **kwargs: Additional query parameters

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if isinstance(media_item_types, list):
            media_item_types = self.SEPERATOR.join(media_item_types)
        url = self.EDS_URL + "/media/%s/singleMediaGroupSearch?" % self.client.language.locale
        params = {
            "q": search_query,
            "maxItems": max_items,
            "desiredMediaItemTypes": media_item_types
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)


class MediaItemType(Enum):
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


class MediaGroup(Enum):
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


class ScheduleDetailsField(Enum):
    """
    Schedule Details Field, used as parameter for EDS API
    """
    NAME = "Name"
    ID = "Id"
    IMAGES = "Images"
    DESCRIPTION = "Description"
    PARENTAL_RATING = "ParentalRating"
    PARENT_SERIES = "ParentSeries"
    SCHEDULE_INFO = "ScheduleInformation"


class Domain(Enum):
    """
    Domain, used as parameter for EDS API
    """
    XBOX_360 = "Xbox360"
    XBOX_ONE = "Modern"


class IdType(Enum):
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


class ClientType(Enum):
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


class DeviceType(Enum):
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
