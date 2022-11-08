from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_get_list(respx_mock, xbl_client):
    route = respx_mock.get("https://eplists.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("lists_get_items"))
    )
    ret = await xbl_client.lists.get_items(xbl_client.xuid)

    assert ret.list_metadata.list_count == 3
    assert route.called


@pytest.mark.asyncio
async def test_list_add(respx_mock, xbl_client):
    route = respx_mock.post("https://eplists.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("list_add_item"))
    )
    post_body = {
        "Items": [
            {
                "Locale": "en-US",
                "ContentType": "DDurable",
                "Title": "Destiny 2: Shadowkeep + Season",
                "ItemId": "361f6d1c-7d72-4b95-8481-92fdf167363f",
                "DeviceType": "XboxOne",
                "ImageUrl": r"https:\/\/store-images.s-microsoft.com\/image\/apps.47381.13678370117067710.1218a7fe-a12c-4b72-ab48-1609d37bb31e.08ee0643-ed52-4e52-9e24-1d944888baf7",
            }
        ]
    }
    ret = await xbl_client.lists.insert_items(xbl_client.xuid, post_body)

    assert ret.list_count == 8
    assert route.called


@pytest.mark.asyncio
async def test_list_delete(respx_mock, xbl_client):
    route = respx_mock.delete("https://eplists.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("list_delete_item"))
    )
    post_body = {
        "Items": [
            {
                "Locale": "en-US",
                "ContentType": "DDurable",
                "Title": "Destiny 2: Shadowkeep + Season",
                "ItemId": "361f6d1c-7d72-4b95-8481-92fdf167363f",
                "DeviceType": "XboxOne",
                "ImageUrl": r"https:\/\/store-images.s-microsoft.com\/image\/apps.47381.13678370117067710.1218a7fe-a12c-4b72-ab48-1609d37bb31e.08ee0643-ed52-4e52-9e24-1d944888baf7",
            }
        ]
    }
    ret = await xbl_client.lists.remove_items(xbl_client.xuid, post_body)

    assert ret.list_count == 7
    assert route.called
