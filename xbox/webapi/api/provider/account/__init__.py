from xbox.webapi.api.provider.baseprovider import BaseProvider


class AccountProvider(BaseProvider):
    BASE_URL_USER_MGT = "https://user.mgt.xboxlive.com"
    BASE_URL_ACCOUNT = "https://accounts.xboxlive.com"

    HEADERS_USER_MGT = {"x-xbl-contract-version": "1"}
    HEADERS_ACCOUNT = {"x-xbl-contract-version": "2"}

    async def claim_gamertag(self, xuid, gamertag):
        """
        Claim gamertag

        XLE error codes:
            400 - Bad API request
            401 - Unauthorized
            409 - Gamertag unavailable
            429 - Too many requests
            200 - Gamertag available

        Args:
            xuid (int): Your xuid as integer
            gamertag (str): Desired gamertag

        Returns:
            object: Instance of :class:`aiohttp.ClientResponse`
        """
        url = self.BASE_URL_USER_MGT + "/gamertags/reserve"
        post_data = {"Gamertag": gamertag, "ReservationId": str(xuid)}
        return await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_USER_MGT
        )

    async def change_gamertag(self, xuid, gamertag, preview=False):
        """
        Change your gamertag.

        XLE error codes:
            200 - success
            1020 - No free gamertag changes available

        Args:
            xuid (int): Your Xuid as integer
            gamertag (str): Desired gamertag name
            preview (bool): Preview the change

        Returns:
            object: Instance of :class:`aiohttp.ClientResponse`
        """
        url = self.BASE_URL_ACCOUNT + "/users/current/profile/gamertag"
        post_data = {
            "gamertag": gamertag,
            "preview": preview,
            "reservationId": int(xuid),
        }
        return await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_ACCOUNT
        )
