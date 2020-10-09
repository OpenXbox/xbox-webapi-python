"""
Gameclips - Get gameclip info
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.gameclips.models import GameclipsResponse


class GameclipProvider(BaseProvider):
    GAMECLIPS_METADATA_URL = "https://gameclipsmetadata.xboxlive.com"
    HEADERS_GAMECLIPS_METADATA = {"x-xbl-contract-version": "1"}

    async def get_recent_community_clips_by_title_id(
        self, title_id: str
    ) -> GameclipsResponse:
        """
        Get recent community clips by Title Id

        Args:
            title_id: Title Id to get clips for

        Returns:
            :class:`GameclipsResponse`: Game clip Response
        """
        url = self.GAMECLIPS_METADATA_URL + f"/public/titles/{title_id}/clips"
        params = {"qualifier": "created"}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA
        )
        resp.raise_for_status()
        return GameclipsResponse.parse_raw(await resp.text())

    async def get_recent_own_clips(
        self, title_id: str = None, skip_items: int = 0, max_items: int = 25
    ) -> GameclipsResponse:
        """
        Get own recent clips, optionally filter for title Id

        Args:
            title_id: Title ID to filter
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns:
            :class:`GameclipsResponse`: Game clip Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/users/me"
        if title_id:
            url += f"/titles/{title_id}"
        url += "/clips"

        params = {"skipItems": skip_items, "maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA
        )
        resp.raise_for_status()
        return GameclipsResponse.parse_raw(await resp.text())

    async def get_recent_clips_by_xuid(
        self, xuid: str, title_id: str = None, skip_items: int = 0, max_items: int = 25
    ) -> GameclipsResponse:
        """
        Get clips by XUID, optionally filter for title Id

        Args:
            xuid: XUID of user to get clips from
            title_id: Optional title id filter
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns:
            :class:`GameclipsResponse`: Game clip Response
        """
        url = self.GAMECLIPS_METADATA_URL + f"/users/xuid({xuid})"
        if title_id:
            url += f"/titles/{title_id}"
        url += "/clips"

        params = {"skipItems": skip_items, "maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA
        )
        resp.raise_for_status()
        return GameclipsResponse.parse_raw(await resp.text())

    async def get_saved_community_clips_by_title_id(
        self, title_id: str
    ) -> GameclipsResponse:
        """
        Get saved community clips by Title Id

        Args:
            title_id: Title Id to get screenshots for

        Returns:
            :class:`GameclipsResponse`: Game clip Response
        """
        url = self.GAMECLIPS_METADATA_URL + f"/public/titles/{title_id}/clips/saved"
        params = {"qualifier": "created"}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA
        )
        resp.raise_for_status()
        return GameclipsResponse.parse_raw(await resp.text())

    async def get_saved_own_clips(
        self, title_id: str = None, skip_items: int = 0, max_items: int = 25
    ) -> GameclipsResponse:
        """
        Get own saved clips, optionally filter for title Id an

        Args:
            title_id: Optional Title ID to filter
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns:
            :class:`GameclipsResponse`: Game clip Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/users/me"
        if title_id:
            url += f"/titles/{title_id}"
        url += "/clips/saved"

        params = {"skipItems": skip_items, "maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA
        )
        resp.raise_for_status()
        return GameclipsResponse.parse_raw(await resp.text())

    async def get_saved_clips_by_xuid(
        self, xuid: str, title_id: str = None, skip_items: int = 0, max_items: int = 25
    ) -> GameclipsResponse:
        """
        Get saved clips by XUID, optionally filter for title Id

        Args:
            xuid: XUID of user to get screenshots from
            title_id: Optional title id filter
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns:
            :class:`GameclipsResponse`: Game clip Response
        """
        url = self.GAMECLIPS_METADATA_URL + f"/users/xuid({xuid})"
        if title_id:
            url += f"/titles/{title_id}"
        url += "/clips/saved"

        params = {"skipItems": skip_items, "maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA
        )
        resp.raise_for_status()
        return GameclipsResponse.parse_raw(await resp.text())
