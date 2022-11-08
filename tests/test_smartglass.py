from httpx import Response
import pytest

from xbox.webapi.api.provider.smartglass.models import InputKeyType, VolumeDirection

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_get_console_list(respx_mock, xbl_client):
    route = respx_mock.get("https://xccs.xboxlive.com/lists/devices").mock(
        return_value=Response(200, json=get_response_json("smartglass_console_list"))
    )
    ret = await xbl_client.smartglass.get_console_list()

    assert len(ret.result) == 2
    assert route.called


@pytest.mark.asyncio
async def test_get_installed_apps(respx_mock, xbl_client):
    route = respx_mock.get("https://xccs.xboxlive.com/lists/installedApps").mock(
        return_value=Response(200, json=get_response_json("smartglass_installed_apps"))
    )
    device_id = "ABCDEFG"
    ret = await xbl_client.smartglass.get_installed_apps(device_id)

    assert len(ret.result) == 2
    assert route.called
    assert device_id in str(respx_mock.calls[0].request.url)


@pytest.mark.asyncio
async def test_get_storage_devices(respx_mock, xbl_client):
    route = respx_mock.get("https://xccs.xboxlive.com/lists/storageDevices").mock(
        return_value=Response(200, json=get_response_json("smartglass_storage_devices"))
    )
    device_id = "ABCDEFG"
    ret = await xbl_client.smartglass.get_storage_devices(device_id)

    assert len(ret.result) == 1
    assert ret.device_id == device_id
    assert route.called
    assert device_id in str(respx_mock.calls[0].request.url)


@pytest.mark.asyncio
async def test_get_console_status(respx_mock, xbl_client):
    route = respx_mock.get("https://xccs.xboxlive.com/consoles/ABCDEFG").mock(
        return_value=Response(200, json=get_response_json("smartglass_console_status"))
    )
    ret = await xbl_client.smartglass.get_console_status("ABCDEFG")

    assert ret.status.error_code == "OK"
    assert route.called


@pytest.mark.asyncio
async def test_get_op_status(respx_mock, xbl_client):
    route = respx_mock.get("https://xccs.xboxlive.com/opStatus").mock(
        return_value=Response(200, json=get_response_json("smartglass_op_status"))
    )
    ret = await xbl_client.smartglass.get_op_status(
        "ABCDEFG", "35bd7870-fad4-4e98-a354-d027bd840116"
    )

    assert ret.status.error_code == "OK"
    assert route.called


@pytest.mark.asyncio
async def test_commands(respx_mock, xbl_client):
    device_args = {"device_id": "ABCDEFG"}
    commands = [
        {"method": "wake_up", "args": {**device_args}},
        {"method": "turn_off", "args": {**device_args}},
        {"method": "reboot", "args": {**device_args}},
        {"method": "mute", "args": {**device_args}},
        {"method": "unmute", "args": {**device_args}},
        {"method": "volume", "args": {**device_args, "direction": VolumeDirection.Up}},
        {"method": "play", "args": {**device_args}},
        {"method": "pause", "args": {**device_args}},
        {"method": "previous", "args": {**device_args}},
        {"method": "next", "args": {**device_args}},
        {"method": "go_home", "args": {**device_args}},
        {"method": "go_back", "args": {**device_args}},
        {"method": "show_guide_tab", "args": {**device_args}},
        {"method": "press_button", "args": {**device_args, "button": InputKeyType.A}},
        {"method": "insert_text", "args": {**device_args, "text": "Test"}},
        {
            "method": "launch_app",
            "args": {**device_args, "one_store_product_id": "9WZDNCRFJ3TJ"},
        },
        {"method": "show_tv_guide", "args": {**device_args}},
    ]
    route = respx_mock.post("https://xccs.xboxlive.com/commands").mock(
        return_value=Response(200, json=get_response_json("smartglass_command"))
    )

    for command in commands:
        await getattr(xbl_client.smartglass, command["method"])(**command["args"])

    assert route.called
