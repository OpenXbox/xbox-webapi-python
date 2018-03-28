"""
CQS

Used for download stump (TV Streaming) data
(RemoteTVInput ServiceChannel on Smartglass)
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.common.enum import StrEnum


class CQSProvider(BaseProvider):
    CQS_URL = "https://cqs.xboxlive.com"
    HEADERS_CQS = {
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Pragma': 'no-cache',
        'x-xbl-client-type': 'Companion',
        'x-xbl-client-version': '2.0',
        'x-xbl-contract-version': '1.b',
        'x-xbl-device-type': 'WindowsPhone',
        'x-xbl-isautomated-client': 'true'
    }

    def get_channel_list(self, locale_info, headend_id):
        """
        Get stump channel list

        Args:
            locale_info (str): Locale string (format: "en-US")
            headend_id (str): Headend id

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.CQS_URL + "/epg/%s/lineups/%s/channels?" % (locale_info, headend_id)
        params = {
            "desired": str(VesperType.MOBILE_LINEUP)
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_CQS)

    def get_schedule(self, locale_info, headend_id, start_date, duration_minutes, channel_skip, channel_count):
        """
        Get stump epg data

        Args:
            locale_info (str): Locale string (format: "en-US")
            headend_id (str): Headend id
            start_date (str): Start date (format: 2016-07-11T21:50:00.000Z)
            duration_minutes (int): Schedule duration to download
            channel_skip (int): Count of channels to skip
            channel_count (int): Count of channels to get data for

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.CQS_URL + "/epg/%s/lineups/%s/programs?" % (locale_info, headend_id)
        params = {
            "startDate": start_date,
            "durationMinutes": duration_minutes,
            "channelSkip": channel_skip,
            "channelCount": channel_count,
            "desired": str(VesperType.MOBILE_SCHEDULE)
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_CQS)


class VesperType(StrEnum):
    MOBILE_LINEUP = "vesper_mobile_lineup"
    MOBILE_SCHEDULE = "vesper_mobile_schedule"
