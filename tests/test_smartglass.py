import pytest

from xbox.webapi.api.provider.smartglass.models import InputKeyType, VolumeDirection

from tests.common import get_response


@pytest.mark.asyncio
async def test_get_console_list(aresponses, xbl_client):
    aresponses.add(
        "xccs.xboxlive.com",
        "/lists/devices",
        response=get_response("smartglass_console_list"),
    )
    ret = await xbl_client.smartglass.get_console_list()
    await xbl_client._auth_mgr.session.close()

    assert len(ret.result) == 2
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_installed_apps(aresponses, xbl_client):
    aresponses.add(
        "xccs.xboxlive.com",
        "/lists/installedApps",
        response=get_response("smartglass_installed_apps"),
    )
    device_id = "ABCDEFG"
    ret = await xbl_client.smartglass.get_installed_apps(device_id)
    await xbl_client._auth_mgr.session.close()

    assert len(ret.result) == 2
    aresponses.assert_plan_strictly_followed()
    assert aresponses.history[0].request.query["deviceId"] == device_id


@pytest.mark.asyncio
async def test_get_storage_devices(aresponses, xbl_client):
    aresponses.add(
        "xccs.xboxlive.com",
        "/lists/storageDevices",
        response=get_response("smartglass_storage_devices"),
    )
    device_id = "ABCDEFG"
    ret = await xbl_client.smartglass.get_storage_devices(device_id)
    await xbl_client._auth_mgr.session.close()

    assert len(ret.result) == 1
    assert ret.device_id == device_id
    aresponses.assert_plan_strictly_followed()
    assert aresponses.history[0].request.query["deviceId"] == device_id


@pytest.mark.asyncio
async def test_get_console_status(aresponses, xbl_client):
    aresponses.add(
        "xccs.xboxlive.com",
        "/consoles/ABCDEFG",
        response=get_response("smartglass_console_status"),
    )
    ret = await xbl_client.smartglass.get_console_status("ABCDEFG")
    await xbl_client._auth_mgr.session.close()

    assert ret.status.error_code == "OK"
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_op_status(aresponses, xbl_client):
    aresponses.add(
        "xccs.xboxlive.com", "/opStatus", response=get_response("smartglass_op_status")
    )
    ret = await xbl_client.smartglass.get_op_status(
        "ABCDEFG", "35bd7870-fad4-4e98-a354-d027bd840116"
    )
    await xbl_client._auth_mgr.session.close()

    assert ret.status.error_code == "OK"
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_commands(aresponses, xbl_client):
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
    aresponses.add(
        "xccs.xboxlive.com",
        "/commands",
        response=get_response("smartglass_command"),
        repeat=len(commands),
    )

    for command in commands:
        await getattr(xbl_client.smartglass, command["method"])(**command["args"])
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()
