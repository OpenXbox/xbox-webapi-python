"""
Profile

Get Userprofiles by XUID or Gamertag
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class ProfileProvider(BaseProvider):
    PROFILE_URL = "https://profile.xboxlive.com"
    HEADERS_PROFILE = {
        'x-xbl-contract-version': '2'
    }
    SEPARATOR = ","

    def get_profiles(self, xuid_list):
        """
        Get profile info for list of xuids

        Args:
            xuid_list (list): List of xuids

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        post_data = {
            "settings": [
                ProfileSettings.GAME_DISPLAY_NAME,
                ProfileSettings.APP_DISPLAY_NAME,
                ProfileSettings.APP_DISPLAYPIC_RAW,
                ProfileSettings.GAMERSCORE,
                ProfileSettings.GAMERTAG,
                ProfileSettings.GAME_DISPLAYPIC_RAW,
                ProfileSettings.ACCOUNT_TIER,
                ProfileSettings.TENURE_LEVEL,
                ProfileSettings.XBOX_ONE_REP,
                ProfileSettings.PREFERRED_COLOR,
                ProfileSettings.LOCATION,
                ProfileSettings.BIOGRAPHY,
                ProfileSettings.WATERMARKS,
                ProfileSettings.REAL_NAME
            ],
            "userIds": [int(xuid) for xuid in xuid_list]
        }
        url = self.PROFILE_URL + "/users/batch/profile/settings"
        return self.client.session.post(url, json=post_data, headers=self.HEADERS_PROFILE)

    def get_profile_by_xuid(self, target_xuid):
        """
        Get Userprofile by xuid

        Args:
            target_xuid (int): XUID to get profile for

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.PROFILE_URL + "/users/xuid(%s)/profile/settings?" % target_xuid
        params = {
            'settings': self.SEPARATOR.join([
                ProfileSettings.APP_DISPLAY_NAME,
                ProfileSettings.GAMERSCORE,
                ProfileSettings.GAMERTAG,
                ProfileSettings.PUBLIC_GAMERPIC,
                ProfileSettings.XBOX_ONE_REP
            ])
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_PROFILE)

    def get_profile_by_gamertag(self, gamertag):
        """
        Get Userprofile by gamertag

        Args:
            gamertag (str): Gamertag to get profile for

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.PROFILE_URL + "/users/gt(%s)/profile/settings?" % gamertag
        params = {
            'settings': self.SEPARATOR.join([
                ProfileSettings.APP_DISPLAY_NAME,
                ProfileSettings.GAMERSCORE,
                ProfileSettings.GAMERTAG,
                ProfileSettings.PUBLIC_GAMERPIC,
                ProfileSettings.XBOX_ONE_REP
            ])
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_PROFILE)


class ProfileSettings(object):
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
    ACCOUNT_TIER = "AccountTier"
    TENURE_LEVEL = "TenureLevel"
    XBOX_ONE_REP = "XboxOneRep"
    PREFERRED_COLOR = "PreferredColor"
    LOCATION = "Location"
    BIOGRAPHY = "Bio"
    WATERMARKS = "Watermarks"
    REAL_NAME = "RealName"
    REAL_NAME_OVERRIDE = "RealNameOverride"
