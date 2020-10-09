"""
Screenshots - Get screenshot info
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.screenshots.models import ScreenshotResponse


class ScreenshotsProvider(BaseProvider):
    SCREENSHOTS_METADATA_URL = "https://screenshotsmetadata.xboxlive.com"
    HEADERS_SCREENSHOTS_METADATA = {"x-xbl-contract-version": "5"}

    async def get_recent_community_screenshots_by_title_id(
        self, title_id: str
    ) -> ScreenshotResponse:
        """
        Get recent community screenshots by Title Id

        Args:
            title_id: Title Id to get screenshots for

        Returns:
            :class:`ScreenshotResponse`: Screenshot Response
        """
        url = self.SCREENSHOTS_METADATA_URL + f"/public/titles/{title_id}/screenshots"
        params = {"qualifier": "created"}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA
        )
        resp.raise_for_status()
        return ScreenshotResponse.parse_raw(await resp.text())

    async def get_recent_own_screenshots(
        self, title_id: str = None, skip_items: int = 0, max_items: int = 25
    ) -> ScreenshotResponse:
        """
        Get own recent screenshots, optionally filter for title Id

        Args:
            title_id: Title ID to filter
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns:
            :class:`ScreenshotResponse`: Screenshot Response
        """
        url = self.SCREENSHOTS_METADATA_URL + "/users/me"
        if title_id:
            url += f"/titles/{title_id}"
        url += "/screenshots"

        params = {"skipItems": skip_items, "maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA
        )
        resp.raise_for_status()
        return ScreenshotResponse.parse_raw(await resp.text())

    async def get_recent_screenshots_by_xuid(
        self, xuid: str, title_id: str = None, skip_items: int = 0, max_items: int = 25
    ) -> ScreenshotResponse:
        """
        Get recent screenshots by XUID, optionally filter for title Id

        Args:
            xuid: XUID of user to get screenshots from
            title_id: Optional title id filter
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns:
            :class:`ScreenshotResponse`: Screenshot Response
        """
        url = self.SCREENSHOTS_METADATA_URL + f"/users/xuid({xuid})"
        if title_id:
            url += f"/titles/{title_id}"
        url += "/screenshots"

        params = {"skipItems": skip_items, "maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA
        )
        resp.raise_for_status()
        return ScreenshotResponse.parse_raw(await resp.text())

    async def get_saved_community_screenshots_by_title_id(
        self, title_id: str
    ) -> ScreenshotResponse:
        """
        Get saved community screenshots by Title Id

        Args:
            title_id: Title Id to get screenshots for

        Returns:
            :class:`ScreenshotResponse`: Screenshot Response
        """
        url = f"{self.SCREENSHOTS_METADATA_URL}/public/titles/{title_id}/screenshots/saved"
        params = {"qualifier": "created"}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA
        )
        resp.raise_for_status()
        return ScreenshotResponse.parse_raw(await resp.text())

    async def get_saved_own_screenshots(
        self, title_id: str = None, skip_items: int = 0, max_items: int = 25
    ) -> ScreenshotResponse:
        """
        Get own saved screenshots, optionally filter for title Id an

        Args:
            title_id: Optional Title ID to filter
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns:
            :class:`ScreenshotResponse`: Screenshot Response
        """
        url = self.SCREENSHOTS_METADATA_URL + "/users/me"
        if title_id:
            url += f"/titles/{title_id}"
        url += "/screenshots/saved"

        params = {"skipItems": skip_items, "maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA
        )
        resp.raise_for_status()
        return ScreenshotResponse.parse_raw(await resp.text())

    async def get_saved_screenshots_by_xuid(
        self, xuid: str, title_id: str = None, skip_items: int = 0, max_items: int = 25
    ) -> ScreenshotResponse:
        """
        Get saved screenshots by XUID, optionally filter for title Id

        Args:
            xuid: XUID of user to get screenshots from
            title_id: Optional title id filter
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns:
            :class:`ScreenshotResponse`: Screenshot Response
        """
        url = self.SCREENSHOTS_METADATA_URL + f"/users/xuid({xuid})"
        if title_id:
            url += f"/titles/{title_id}"
        url += "/screenshots/saved"

        params = {"skipItems": skip_items, "maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA
        )
        resp.raise_for_status()
        return ScreenshotResponse.parse_raw(await resp.text())
