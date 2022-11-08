from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_get_inbox(respx_mock, xbl_client):
    route = respx_mock.get("https://xblmessaging.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("message_get_inbox"))
    )
    await xbl_client.message.get_inbox()

    assert route.called


@pytest.mark.asyncio
async def test_get_conversation(respx_mock, xbl_client):
    route = respx_mock.get("https://xblmessaging.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("message_get_conversation"))
    )
    await xbl_client.message.get_conversation(
        "05907fa3-0000-0009-acbd-299772a90900"
    )

    assert route.called


@pytest.mark.asyncio
async def test_get_new_conversation(respx_mock, xbl_client):
    route = respx_mock.get("https://xblmessaging.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("message_new_conversation"))
    )
    await xbl_client.message.get_conversation(
        "05907fa3-0000-0009-acbd-299772a90900"
    )

    assert route.called


@pytest.mark.asyncio
async def test_delete_conversation(respx_mock, xbl_client):
    route = respx_mock.put("https://xblmessaging.xboxlive.com").mock(
        return_value=Response(200)
    )
    ret = await xbl_client.message.delete_conversation(
        "05907fa3-0000-0009-acbd-299772a90900", "14670705998559210"
    )

    assert ret is True
    assert route.called


@pytest.mark.asyncio
async def test_delete_message(respx_mock, xbl_client):
    route = respx_mock.delete("https://xblmessaging.xboxlive.com").mock(
        return_value=Response(200)
    )
    ret = await xbl_client.message.delete_message(
        "05907fa3-0000-0009-acbd-299772a90900", "14670705998559210"
    )

    assert ret is True
    assert route.called


@pytest.mark.asyncio
async def test_send_message(respx_mock, xbl_client):
    route = respx_mock.post("https://xblmessaging.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("message_send_message"))
    )
    ret = await xbl_client.message.send_message("12345", "Test message")

    assert ret.conversation_id
    assert ret.message_id
    assert route.called


@pytest.mark.asyncio
async def test_message_send_too_long(xbl_client):
    message = "x" * 257
    with pytest.raises(ValueError) as err:
        await xbl_client.message.send_message("12345", message)

    assert "exceeds max length" in str(err)
