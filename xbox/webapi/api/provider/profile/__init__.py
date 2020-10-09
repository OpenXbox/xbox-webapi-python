"""
Profile

Get Userprofiles by XUID or Gamertag
"""
from typing import List

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.profile.models import ProfileResponse, ProfileSettings


class ProfileProvider(BaseProvider):
    PROFILE_URL = "https://profile.xboxlive.com"
    HEADERS_PROFILE = {"x-xbl-contract-version": "3"}
    SEPARATOR = ","

    async def get_profiles(self, xuid_list: List[str]) -> ProfileResponse:
        """
        Get profile info for list of xuids

        Args:
            xuid_list (list): List of xuids

        Returns:
            :class:`ProfileResponse`: Profile Response
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
                ProfileSettings.REAL_NAME,
            ],
            "userIds": xuid_list,
        }
        url = self.PROFILE_URL + "/users/batch/profile/settings"
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_PROFILE
        )
        resp.raise_for_status()
        return ProfileResponse.parse_raw(await resp.text())

    async def get_profile_by_xuid(self, target_xuid: str) -> ProfileResponse:
        """
        Get Userprofile by xuid

        Args:
            target_xuid: XUID to get profile for

        Returns:
            :class:`ProfileResponse`: Profile Response
        """
        url = self.PROFILE_URL + f"/users/xuid({target_xuid})/profile/settings"
        params = {
            "settings": self.SEPARATOR.join(
                [
                    ProfileSettings.GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG_SUFFIX,
                    ProfileSettings.UNIQUE_MODERN_GAMERTAG,
                    ProfileSettings.REAL_NAME_OVERRIDE,
                    ProfileSettings.BIOGRAPHY,
                    ProfileSettings.LOCATION,
                    ProfileSettings.GAMERSCORE,
                    ProfileSettings.GAME_DISPLAYPIC_RAW,
                    ProfileSettings.TENURE_LEVEL,
                    ProfileSettings.ACCOUNT_TIER,
                    ProfileSettings.XBOX_ONE_REP,
                    ProfileSettings.PREFERRED_COLOR,
                    ProfileSettings.WATERMARKS,
                    ProfileSettings.IS_QUARANTINED,
                ]
            )
        }
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_PROFILE
        )
        resp.raise_for_status()
        return ProfileResponse.parse_raw(await resp.text())

    async def get_profile_by_gamertag(self, gamertag: str) -> ProfileResponse:
        """
        Get Userprofile by gamertag

        Args:
            gamertag: Gamertag to get profile for

        Returns:
            :class:`ProfileResponse`: Profile Response
        """
        url = self.PROFILE_URL + f"/users/gt({gamertag})/profile/settings"
        params = {
            "settings": self.SEPARATOR.join(
                [
                    ProfileSettings.GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG_SUFFIX,
                    ProfileSettings.UNIQUE_MODERN_GAMERTAG,
                    ProfileSettings.REAL_NAME_OVERRIDE,
                    ProfileSettings.BIOGRAPHY,
                    ProfileSettings.LOCATION,
                    ProfileSettings.GAMERSCORE,
                    ProfileSettings.GAME_DISPLAYPIC_RAW,
                    ProfileSettings.TENURE_LEVEL,
                    ProfileSettings.ACCOUNT_TIER,
                    ProfileSettings.XBOX_ONE_REP,
                    ProfileSettings.PREFERRED_COLOR,
                    ProfileSettings.WATERMARKS,
                    ProfileSettings.IS_QUARANTINED,
                ]
            )
        }
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_PROFILE
        )
        resp.raise_for_status()
        return ProfileResponse.parse_raw(await resp.text())
