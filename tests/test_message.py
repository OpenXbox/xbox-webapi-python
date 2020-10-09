import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_get_inbox(aresponses, xbl_client):
    aresponses.add(
        "xblmessaging.xboxlive.com", response=get_response("message_get_inbox")
    )
    ret = await xbl_client.message.get_inbox()
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_conversation(aresponses, xbl_client):
    aresponses.add(
        "xblmessaging.xboxlive.com", response=get_response("message_get_conversation")
    )
    ret = await xbl_client.message.get_conversation(
        "05907fa3-0000-0009-acbd-299772a90900"
    )
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_new_conversation(aresponses, xbl_client):
    aresponses.add(
        "xblmessaging.xboxlive.com", response=get_response("message_new_conversation")
    )
    ret = await xbl_client.message.get_conversation(
        "05907fa3-0000-0009-acbd-299772a90900"
    )
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_delete_conversation(aresponses, xbl_client):
    aresponses.add(
        "xblmessaging.xboxlive.com",
        method_pattern="PUT",
        response=aresponses.Response(status=200),
    )
    ret = await xbl_client.message.delete_conversation(
        "05907fa3-0000-0009-acbd-299772a90900", "14670705998559210"
    )
    await xbl_client._auth_mgr.session.close()

    assert ret is True
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_delete_message(aresponses, xbl_client):
    aresponses.add(
        "xblmessaging.xboxlive.com",
        method_pattern="DELETE",
        response=aresponses.Response(status=200),
    )
    ret = await xbl_client.message.delete_message(
        "05907fa3-0000-0009-acbd-299772a90900", "14670705998559210"
    )
    await xbl_client._auth_mgr.session.close()

    assert ret is True
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_send_message(aresponses, xbl_client):
    aresponses.add(
        "xblmessaging.xboxlive.com",
        method_pattern="POST",
        response=get_response("message_send_message"),
    )
    ret = await xbl_client.message.send_message("12345", "Test message")
    await xbl_client._auth_mgr.session.close()

    assert ret.conversation_id
    assert ret.message_id
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_message_send_too_long(xbl_client):
    message = "x" * 257
    with pytest.raises(ValueError) as err:
        await xbl_client.message.send_message("12345", message)

    assert "exceeds max length" in str(err)
    await xbl_client._auth_mgr.session.close()
