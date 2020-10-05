"""
EDS (Entertainment Discovery Services)

Used for searching the Xbox Live Marketplace
"""
from typing import List

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.eds.models import (
    EDSResponse,
    MediaGroup,
    MediaItemType,
    OrderBy,
    ScheduleDetailsField,
)


class EDSProvider(BaseProvider):
    EDS_URL = "https://eds.xboxlive.com"
    HEADERS_EDS = {
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Pragma": "no-cache",
        "x-xbl-client-type": "Companion",
        "x-xbl-client-version": "2.0",
        "x-xbl-contract-version": "3.2",
        "x-xbl-device-type": "WindowsPhone",
        "x-xbl-isautomated-client": "true",
    }

    SEPERATOR = "."

    async def get_appchannel_channel_list(self, lineup_id):
        """
        Get AppChannel channel list

        Args:
            lineup_id (str): Lineup ID

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.EDS_URL + f"/media/{self.client.language.locale}/tvchannels"
        params = {"channelLineupId": lineup_id}
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_EDS
        )

    async def get_appchannel_schedule(
        self,
        lineup_id: str,
        start_time: str,
        end_time: str,
        max_items: int,
        skip_items: int,
    ):
        """
        Get AppChannel schedule / EPG

        Args:
            lineup_id: Lineup ID
            start_time: Start time (format: 2016-07-11T21:50:00.000Z)
            end_time: End time (format: 2016-07-11T21:50:00.000Z)
            max_items: Maximum number of items
            skip_items: Count of items to skip

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = f"{self.EDS_URL}/media/{self.client.language.locale}/tvchannellineupguide"
        desired = [
            ScheduleDetailsField.ID,
            ScheduleDetailsField.NAME,
            ScheduleDetailsField.IMAGES,
            ScheduleDetailsField.DESCRIPTION,
            ScheduleDetailsField.PARENTAL_RATING,
            ScheduleDetailsField.PARENT_SERIES,
            ScheduleDetailsField.SCHEDULE_INFO,
        ]
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "maxItems": max_items,
            "skipItems": skip_items,
            "channelLineupId": lineup_id,
            "desired": self.SEPERATOR.join(d.value for d in desired),
        }
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_EDS
        )

    async def get_browse_query(
        self, order_by: List[OrderBy], desired: List[MediaItemType], **kwargs
    ):
        """
        Get a browse query

        Args:
            order_by: Fieldname to use for sorting the result
            desired: Desired Media Item Types
            **kwargs: Additional query parameters

        Returns:

        """
        order_by = self.SEPERATOR.join(o.value for o in order_by)
        desired = self.SEPERATOR.join(d.value for d in desired)

        url = self.EDS_URL + f"/media/{self.client.language.locale}/browse"
        params = {
            "fields": "all",
            "orderBy": order_by,
            "desiredMediaItemTypes": desired,
        }
        params.update(kwargs)
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_EDS
        )

    async def get_recommendations(self, desired: List[MediaItemType], **kwargs):
        """
        Get recommended content suggestions

        Args:
            desired: Desired Media Item Types
            **kwargs: Additional query parameters

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        if isinstance(desired, list):
            desired = self.SEPERATOR.join(d.value for d in desired)

        url = self.EDS_URL + f"/media/{self.client.language.locale}/recommendations"
        params = {"desiredMediaItemTypes": desired}
        params.update(kwargs)
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_EDS
        )

    async def get_related(self, id: str, desired: List[MediaItemType], **kwargs):
        """
        Get related content for a specific Id

        Args:
            id: Id of original content to get related content for
            desired: Desired Media Item Types
            **kwargs: Additional query parameters

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        desired = self.SEPERATOR.join(d.value for d in desired)

        url = self.EDS_URL + f"/media/{self.client.language.locale}/related"
        params = {"id": id, "desiredMediaItemTypes": desired}
        params.update(kwargs)
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_EDS
        )

    async def get_fields(self, desired: str, **kwargs):
        """
        Get Fields

        Args:
            desired: Desired
            **kwargs: Additional query parameters

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        if isinstance(desired, list):
            desired = self.SEPERATOR.join(desired)

        url = self.EDS_URL + f"/media/{self.client.language.locale}/fields"
        params = {"desired": desired}
        params.update(kwargs)
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_EDS
        )

    async def get_details(self, ids: List[str], mediagroup: MediaGroup, **kwargs):
        """
        Get details for a list of IDs in a specific media group

        Args:
            ids: List of ids to get details for
            mediagroup: Media group
            **kwargs: Additional query parameters

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        if isinstance(ids, list):
            ids = self.SEPERATOR.join(ids)

        url = self.EDS_URL + f"/media/{self.client.language.locale}/details"
        params = {"ids": ids, "MediaGroup": mediagroup.value}
        params.update(kwargs)
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_EDS
        )

    async def get_crossmediagroup_search(
        self, search_query: str, max_items: int, **kwargs
    ) -> EDSResponse:
        """
        Do a crossmedia-group search (search for content for multiple devices)

        Args:
            search_query: Query string
            max_items: Maximum itemcount
            **kwargs: Additional query parameters

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = (
            f"{self.EDS_URL}/media/{self.client.language.locale}/crossMediaGroupSearch"
        )
        params = {"q": search_query, "maxItems": max_items}
        params.update(kwargs)
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_EDS
        )

    async def get_singlemediagroup_search(
        self,
        search_query: str,
        max_items: int,
        media_item_types: List[MediaItemType],
        **kwargs,
    ) -> EDSResponse:
        """
        Do a singlemedia-group search

        Args:
            search_query: Query string
            max_items: Maximum itemcount
            media_item_types: Desired Media Item Types
            **kwargs: Additional query parameters

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        media_item_types = self.SEPERATOR.join(t.value for t in media_item_types)

        url = (
            f"{self.EDS_URL}/media/{self.client.language.locale}/singleMediaGroupSearch"
        )
        params = {
            "q": search_query,
            "maxItems": max_items,
            "desiredMediaItemTypes": str(media_item_types),
        }
        params.update(kwargs)
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_EDS
        )
