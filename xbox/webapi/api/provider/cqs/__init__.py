"""
CQS

Used for download stump (TV Streaming) data
(RemoteTVInput ServiceChannel on Smartglass)
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.cqs.models import (
    CqsChannelListResponse,
    CqsScheduleResponse,
)


class CQSProvider(BaseProvider):
    CQS_URL = "https://cqs.xboxlive.com"
    HEADERS_CQS = {
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Pragma": "no-cache",
        "x-xbl-client-type": "Companion",
        "x-xbl-client-version": "2.0",
        "x-xbl-contract-version": "1.b",
        "x-xbl-device-type": "WindowsPhone",
        "x-xbl-isautomated-client": "true",
    }

    async def get_channel_list(
        self, locale_info: str, headend_id: str
    ) -> CqsChannelListResponse:
        """
        Get stump channel list

        Args:
            locale_info: Locale string (format: "en-US")
            headend_id: Headend id

        Returns:
            :class:`CqsChannelListResponse`: Channel List Response
        """
        url = self.CQS_URL + f"/epg/{locale_info}/lineups/{headend_id}/channels"
        params = {"desired": "vesper_mobile_lineup"}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_CQS
        )
        resp.raise_for_status()
        return CqsChannelListResponse.parse_raw(await resp.text())

    async def get_schedule(
        self,
        locale_info: str,
        headend_id: str,
        start_date: str,
        duration_minutes: int,
        channel_skip: int,
        channel_count: int,
    ) -> CqsScheduleResponse:
        """
        Get stump epg data

        Args:
            locale_info: Locale string (format: "en-US")
            headend_id: Headend id
            start_date: Start date (format: 2016-07-11T21:50:00.000Z)
            duration_minutes: Schedule duration to download
            channel_skip: Count of channels to skip
            channel_count: Count of channels to get data for

        Returns:
            :class:`CqsScheduleResponse`: Schedule Response
        """
        url = self.CQS_URL + f"/epg/{locale_info}/lineups/{headend_id}/programs"
        params = {
            "startDate": start_date,
            "durationMinutes": duration_minutes,
            "channelSkip": channel_skip,
            "channelCount": channel_count,
            "desired": "vesper_mobile_schedule",
        }
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_CQS
        )
        resp.raise_for_status()
        return CqsScheduleResponse.parse_raw(await resp.text())
