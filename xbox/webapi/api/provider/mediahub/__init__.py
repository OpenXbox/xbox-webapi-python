"""
Mediahub - Fetch screenshots and gameclips
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.mediahub.models import (
    MediahubGameclips,
    MediahubScreenshots,
)


class MediahubProvider(BaseProvider):
    MEDIAHUB_URL = "https://mediahub.xboxlive.com"
    HEADERS = {"x-xbl-contract-version": "3"}

    async def fetch_own_clips(
        self, skip: int = 0, count: int = 500, **kwargs
    ) -> MediahubGameclips:
        """
        Fetch own clips

        Args:
            skip: Number of items to skip
            count: Max entries to fetch

        Returns:
            :class:`MediahubGameclips`: Gameclips
        """
        url = f"{self.MEDIAHUB_URL}/gameclips/search"
        post_data = {
            "max": count,
            "query": f"OwnerXuid eq {self.client.xuid}",
            "skip": skip,
        }
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS, **kwargs
        )
        resp.raise_for_status()
        return MediahubGameclips(**resp.json())

    async def fetch_own_screenshots(
        self, skip: int = 0, count: int = 500, **kwargs
    ) -> MediahubScreenshots:
        """
        Fetch own screenshots

        Args:
            skip: Number of items to skip
            count: Max entries to fetch

        Returns:
            :class:`MediahubScreenshots`: Screenshots
        """
        url = f"{self.MEDIAHUB_URL}/screenshots/search"
        post_data = {
            "max": count,
            "query": f"OwnerXuid eq {self.client.xuid}",
            "skip": skip,
        }
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS, **kwargs
        )
        resp.raise_for_status()
        return MediahubScreenshots(**resp.json())
