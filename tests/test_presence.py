import pytest
from httpx import Response
from tests.common import get_response_json

@pytest.mark.asyncio
async def test_presence(respx_mock, xbl_client):
    route = respx_mock.get("https://userpresence.xboxlive.com").mock(return_value=Response(200, json=get_response_json("presence")))
    ret = await xbl_client.presence.get_presence("2669321029139235")
    
    assert route.called

@pytest.mark.asyncio
async def test_presence_batch(respx_mock, xbl_client):
    route = respx_mock.post("https://userpresence.xboxlive.com").mock(return_value=Response(200, json=get_response_json("presence_batch")))
    ret = await xbl_client.presence.get_presence_batch(
        ["2669321029139235", "2584878536129841"]
    )
    
    assert len(ret) == 2
    assert route.called


@pytest.mark.asyncio
async def test_presence_too_many_people(xbl_client):
    xuids = range(0, 2000)
    with pytest.raises(Exception) as err:
        await xbl_client.presence.get_presence_batch(xuids)

    assert "length is > 1100" in str(err)
    

@pytest.mark.asyncio
async def test_presence_own(respx_mock, xbl_client):
    route = respx_mock.get("https://userpresence.xboxlive.com").mock(return_value=Response(200, json=get_response_json("presence_own")))
    ret = await xbl_client.presence.get_presence_own()
    
    assert route.called
