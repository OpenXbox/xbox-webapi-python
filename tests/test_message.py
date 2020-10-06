import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_message_get_inbox(aresponses, xbl_client):
    aresponses.add(
        "msg.xboxlive.com", response=get_response("message_get_message_inbox")
    )
    ret = await xbl_client.message.get_message_inbox(skip_items=0, max_items=100)
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_message_get_message(aresponses, xbl_client):
    aresponses.add("msg.xboxlive.com", response=get_response("message_get_message"))
    ret = await xbl_client.message.get_message("1")
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_message_delete_msg(aresponses, xbl_client):
    aresponses.add(
        "msg.xboxlive.com",
        method_pattern="DELETE",
        response=aresponses.Response(status=204),
    )
    ret = await xbl_client.message.delete_message("1")
    await xbl_client._auth_mgr.session.close()

    assert ret is True
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_message_send_gt(aresponses, xbl_client):
    aresponses.add(
        "msg.xboxlive.com",
        method_pattern="POST",
        response=aresponses.Response(status=200),
    )
    ret = await xbl_client.message.send_message(
        message_text="Test string", gamertags=["NoExist1", "NoExist2"]
    )
    await xbl_client._auth_mgr.session.close()

    assert ret is True
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_message_send_xuid(aresponses, xbl_client):
    aresponses.add(
        "msg.xboxlive.com",
        method_pattern="POST",
        response=aresponses.Response(status=200),
    )
    ret = await xbl_client.message.send_message(
        message_text="Test string", xuids=["1235", "23533"]
    )
    await xbl_client._auth_mgr.session.close()

    assert ret is True
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_message_send_too_long(xbl_client):
    message = "x" * 257
    with pytest.raises(ValueError) as err:
        await xbl_client.message.send_message(
            message_text=message, gamertags=["NoExist1", "NoExist2"]
        )

    assert "exceeds max length" in str(err)
    await xbl_client._auth_mgr.session.close()


@pytest.mark.asyncio
async def test_message_send_both_gt_xuid(xbl_client):
    with pytest.raises(ValueError) as err:
        await xbl_client.message.send_message(
            message_text="Test string",
            gamertags=["NoExist1", "NoExist2"],
            xuids=[1246, 1263],
        )

    assert "not both" in str(err)
    await xbl_client._auth_mgr.session.close()


@pytest.mark.asyncio
async def test_message_send_nobody(xbl_client):
    with pytest.raises(ValueError) as err:
        await xbl_client.message.send_message(message_text="Test string")

    assert "No recipients" in str(err)
    await xbl_client._auth_mgr.session.close()
