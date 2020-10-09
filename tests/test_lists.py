import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_get_list(aresponses, xbl_client):
    aresponses.add(
        "eplists.xboxlive.com",
        method_pattern="GET",
        response=get_response("lists_get_items"),
    )
    ret = await xbl_client.lists.get_items(xbl_client.xuid)
    await xbl_client._auth_mgr.session.close()

    assert ret.list_metadata.list_count == 3
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_list_add(aresponses, xbl_client):
    aresponses.add(
        "eplists.xboxlive.com",
        method_pattern="POST",
        response=get_response("list_add_item"),
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
    await xbl_client._auth_mgr.session.close()

    assert ret.list_count == 8
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_list_delete(aresponses, xbl_client):
    aresponses.add(
        "eplists.xboxlive.com",
        method_pattern="DELETE",
        response=get_response("list_delete_item"),
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
    await xbl_client._auth_mgr.session.close()

    assert ret.list_count == 7
    aresponses.assert_plan_strictly_followed()
