from datetime import datetime, timedelta, timezone
import uuid

from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_get_device_token(respx_mock, xal_mgr):
    route = respx_mock.post(
        "https://device.auth.xboxlive.com/device/authenticate"
    ).mock(return_value=Response(200, json=get_response_json("auth_device_token")))
    resp = await xal_mgr.request_device_token(
        uuid.UUID("9c493431-5462-4a4a-a247-f6420396318d")
    )
    assert route.called
